import streamlit as st
import time
import pandas as pd

st.title(":material/chat: AI Chatbot")

# Check if data is available
has_data = st.session_state.df is not None

# Provider selection
col1, col2 = st.columns([3, 1])
with col1:
    if has_data:
        st.success(f"Connected to data: {st.session_state.uploaded_filename}", icon=":material/database:")
        st.caption("Ask questions about your data!")
    else:
        st.markdown("Chat with state-of-the-art AI models with real-time streaming responses.")
with col2:
    provider = st.selectbox(
        "Provider",
        ["OpenAI", "Anthropic"],
        key="chat_provider",
        index=0 if st.session_state.llm_provider == "OpenAI" else 1
    )
    st.session_state.llm_provider = provider

# Model selection based on provider
if provider == "OpenAI":
    model = st.selectbox(
        "Model",
        ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
        key="openai_model"
    )
else:
    model = st.selectbox(
        "Model",
        ["claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022", "claude-3-opus-20240229"],
        key="anthropic_model"
    )

# Clear chat button
if st.button(":material/delete: Clear Chat", use_container_width=False):
    st.session_state.messages = []
    st.rerun()

# Show data-aware info
if has_data:
    st.info(f"""
    
    
    The chatbot can now answer questions about your uploaded data ({st.session_state.uploaded_filename}).
    
    **Try asking:**
    - "What are the column names?"
    - "What's the average value of [column]?"
    - "How many rows have missing values?"
    - "Show me the top 5 values in [column]"
    - "What patterns do you see in the data?"
    """, icon=":material/tips_and_updates:")

st.divider()

# Initialize messages if empty
if not st.session_state.messages:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

def prepare_data_context() -> str:
    """Prepare a context summary of the uploaded data."""
    if st.session_state.df is None:
        return ""
    
    df = st.session_state.df
    
    # Basic info
    context = f"\n\n--- UPLOADED DATA CONTEXT ---\n"
    context += f"File: {st.session_state.uploaded_filename}\n"
    context += f"Rows: {len(df)}, Columns: {len(df.columns)}\n\n"
    
    # Column information
    context += "Columns:\n"
    for col in df.columns:
        dtype = df[col].dtype
        null_count = df[col].isnull().sum()
        if dtype in ['int64', 'float64']:
            context += f"- {col} ({dtype}): min={df[col].min():.2f}, max={df[col].max():.2f}, mean={df[col].mean():.2f}, null={null_count}\n"
        else:
            unique_count = df[col].nunique()
            context += f"- {col} ({dtype}): {unique_count} unique values, null={null_count}\n"
    
    # Sample data (first 3 rows)
    context += f"\nFirst 3 rows:\n{df.head(3).to_string()}\n"
    
    # Summary statistics for numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) > 0:
        context += f"\nNumeric Summary:\n{df[numeric_cols].describe().to_string()}\n"
    
    context += "--- END DATA CONTEXT ---\n\n"
    
    return context


# LLM API functions with caching
@st.cache_data(show_spinner=False)
def call_openai(messages_list: list, model_name: str) -> str:
    """Call OpenAI API with caching."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
        
        response = client.chat.completions.create(
            model=model_name,
            messages=messages_list
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error calling OpenAI API: {str(e)}"

@st.cache_data(show_spinner=False)
def call_anthropic(messages_list: list, model_name: str) -> str:
    """Call Anthropic API with caching."""
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY", ""))
        
        response = client.messages.create(
            model=model_name,
            max_tokens=4096,
            messages=messages_list
        )
        return response.content[0].text
    except Exception as e:
        return f"Error calling Anthropic API: {str(e)}"

def stream_openai_response(messages_list: list, model_name: str):
    """Stream OpenAI responses in real-time."""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=st.secrets.get("OPENAI_API_KEY", ""))
        
        stream = client.chat.completions.create(
            model=model_name,
            messages=messages_list,
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"Error: {str(e)}"

def stream_anthropic_response(messages_list: list, model_name: str):
    """Stream Anthropic responses in real-time."""
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=st.secrets.get("ANTHROPIC_API_KEY", ""))
        
        with client.messages.stream(
            model=model_name,
            max_tokens=4096,
            messages=messages_list
        ) as stream:
            for text in stream.text_stream:
                yield text
    except Exception as e:
        yield f"Error: {str(e)}"

# Chat input
if prompt := st.chat_input("Your message"):
    # Check for API keys
    if provider == "OpenAI" and not st.secrets.get("OPENAI_API_KEY"):
        st.error("Please add your OpenAI API key in Settings first!", icon=":material/error:")
        st.stop()
    elif provider == "Anthropic" and not st.secrets.get("ANTHROPIC_API_KEY"):
        st.error("Please add your Anthropic API key in Settings first!", icon=":material/error:")
        st.stop()
    
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Prepare messages for API with data context
    api_messages = []
    
    # Add system message with data context if available
    data_context = ""
    if has_data:
        data_context = prepare_data_context()
        system_content = f"""You are a helpful AI assistant with access to the user's uploaded data. 
Use the data context below to answer questions accurately.

{data_context}

When answering questions about the data:
- Reference specific columns, values, and statistics
- Provide precise numerical answers when possible
- Suggest relevant analyses or visualizations
- If the question isn't about the data, answer normally"""
        
        if provider == "OpenAI":
            # OpenAI supports system messages
            api_messages.append({"role": "system", "content": system_content})
    
    # Add conversation history
    for i, m in enumerate(st.session_state.messages):
        # For Anthropic, prepend data context to first user message only
        if provider == "Anthropic" and has_data and i == 0 and m["role"] == "user":
            api_messages.append({
                "role": m["role"], 
                "content": f"{system_content}\n\n{m['content']}"
            })
        else:
            api_messages.append({"role": m["role"], "content": m["content"]})
    
    # Get and display assistant response with streaming
    with st.chat_message("assistant"):
        if provider == "OpenAI":
            response = st.write_stream(stream_openai_response(api_messages, model))
        else:
            response = st.write_stream(stream_anthropic_response(api_messages, model))
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar with chat stats
with st.sidebar:
    st.subheader(":material/analytics: Chat Statistics")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Current Provider", provider)
    st.metric("Current Model", model)
    
    if has_data:
        st.divider()
        st.subheader(":material/database: Data Context")
        st.success("Active", icon=":material/check_circle:")
        df = st.session_state.df
        st.metric("Dataset", st.session_state.uploaded_filename)
        st.metric("Rows", len(df))
        st.metric("Columns", len(df.columns))
        
        with st.expander("View Data Summary"):
            st.caption("Chatbot has access to:")
            st.dataframe(df.head(3), use_container_width=True)
    else:
        st.divider()
        st.info("Upload data in Data Analysis to enable chat", icon=":material/info:")
    
    if st.session_state.messages:
        st.divider()
        user_msgs = sum(1 for m in st.session_state.messages if m["role"] == "user")
        assistant_msgs = sum(1 for m in st.session_state.messages if m["role"] == "assistant")
        st.metric("User Messages", user_msgs)
        st.metric("AI Responses", assistant_msgs)
