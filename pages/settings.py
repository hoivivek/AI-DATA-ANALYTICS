import streamlit as st
import os
from pathlib import Path

st.title(":material/settings: Settings")

st.markdown("Configure your API keys and application preferences.")

st.divider()

# API Keys Section
st.subheader(":material/key: API Keys")

st.info("""
API keys are stored securely in `.streamlit/secrets.toml`. 
This file is automatically excluded from version control.
""", icon=":material/info:")

# Check if secrets file exists
secrets_dir = Path(".streamlit")
secrets_file = secrets_dir / "secrets.toml"

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("**OpenAI API Key**")
        
        current_openai = st.secrets.get("OPENAI_API_KEY", "")
        if current_openai:
            st.success("Key configured", icon=":material/check_circle:")
            st.caption(f"Key: ...{current_openai[-8:]}")
            
            if st.button("Remove OpenAI Key", key="remove_openai"):
                st.warning("To remove, edit `.streamlit/secrets.toml` manually")
        else:
            st.warning("Not configured", icon=":material/warning:")
        
        openai_key = st.text_input(
            "Enter OpenAI API Key",
            type="password",
            key="openai_input",
            placeholder="sk-..."
        )
        
        if st.button("Save OpenAI Key", key="save_openai"):
            if openai_key:
                st.info("To save: Add to `.streamlit/secrets.toml`:")
                st.code(f'OPENAI_API_KEY = "{openai_key}"')
            else:
                st.error("Please enter a key")

with col2:
    with st.container(border=True):
        st.markdown("**Anthropic API Key**")
        
        current_anthropic = st.secrets.get("ANTHROPIC_API_KEY", "")
        if current_anthropic:
            st.success("Key configured", icon=":material/check_circle:")
            st.caption(f"Key: ...{current_anthropic[-8:]}")
            
            if st.button("Remove Anthropic Key", key="remove_anthropic"):
                st.warning("To remove, edit `.streamlit/secrets.toml` manually")
        else:
            st.warning("Not configured", icon=":material/warning:")
        
        anthropic_key = st.text_input(
            "Enter Anthropic API Key",
            type="password",
            key="anthropic_input",
            placeholder="sk-ant-..."
        )
        
        if st.button("Save Anthropic Key", key="save_anthropic"):
            if anthropic_key:
                st.info("To save: Add to `.streamlit/secrets.toml`:")
                st.code(f'ANTHROPIC_API_KEY = "{anthropic_key}"')
            else:
                st.error("Please enter a key")

st.divider()



# App Preferences
st.subheader(":material/tune: Application Preferences")

with st.form("preferences_form"):
    st.markdown("**Display Settings**")
    
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark", "Auto"],
        help="UI theme preference"
    )
    
    default_chart = st.selectbox(
        "Default Chart Type",
        ["Bar Chart", "Line Chart", "Scatter Plot"],
        help="Default visualization type for dashboard"
    )
    
    st.markdown("**Data Settings**")
    
    max_rows = st.number_input(
        "Max rows to display",
        min_value=10,
        max_value=10000,
        value=100,
        step=10
    )
    
    auto_analyze = st.checkbox(
        "Auto-analyze uploaded data",
        value=True,
        help="Automatically generate statistics when data is uploaded"
    )
    
    st.markdown("**AI Settings**")
    
    default_provider = st.selectbox(
        "Default LLM Provider",
        ["OpenAI", "Anthropic"]
    )
    
    streaming = st.checkbox(
        "Enable streaming responses",
        value=True,
        help="Show AI responses as they're generated"
    )
    
    submitted = st.form_submit_button("Save Preferences", use_container_width=True)
    
    if submitted:
        st.success("Preferences saved! (Note: This is a demo - preferences persist in session only)", icon=":material/check_circle:")
        
        # In a real app, you'd save these to a config file or database
        st.session_state.preferences = {
            "theme": theme,
            "default_chart": default_chart,
            "max_rows": max_rows,
            "auto_analyze": auto_analyze,
            "default_provider": default_provider,
            "streaming": streaming
        }

st.divider()

# System Information
st.subheader(":material/info: System Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Python Version", f"{os.sys.version_info.major}.{os.sys.version_info.minor}")

with col2:
    import streamlit as st_version
    st.metric("Streamlit Version", st_version.__version__)

with col3:
    if st.session_state.df is not None:
        st.metric("Loaded Dataset", st.session_state.uploaded_filename or "Unknown")
    else:
        st.metric("Loaded Dataset", "None")

# Session State Debug (optional)
with st.expander(":material/bug_report: Debug: Session State", expanded=False):
    st.json({
        "messages_count": len(st.session_state.messages),
        "has_data": st.session_state.df is not None,
        "uploaded_file": st.session_state.uploaded_filename,
        "llm_provider": st.session_state.llm_provider,
    })
