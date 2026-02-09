import streamlit as st

st.title(":material/rocket: AI Data Analytics Dashboard")

st.markdown("""
Welcome to your comprehensive AI and data analysis platform! This app combines multiple powerful features:
""")

col1, col2, col3 = st.columns(3)

with col1:
    with st.container(border=True):
        st.subheader(":material/chat: AI Chatbot")
        st.write("Chat with OpenAI GPT-4 or Anthropic Claude with streaming responses.")
        st.page_link("pages/chatbot.py", label="Open Chatbot", icon=":material/arrow_forward:")

with col2:
    with st.container(border=True):
        st.subheader(":material/table_chart: Data Analysis")
        st.write("Upload CSV or JSON files for instant analysis and insights.")
        st.page_link("pages/data_analysis.py", label="Analyze Data", icon=":material/arrow_forward:")

with col3:
    with st.container(border=True):
        st.subheader(":material/bar_chart: Dashboard")
        st.write("Interactive visualizations and charts for your data.")
        st.page_link("pages/dashboard.py", label="View Dashboard", icon=":material/arrow_forward:")

st.divider()

col4, col5 = st.columns(2)

with col4:
    with st.container(border=True):
        st.subheader(":material/cloud: API Tools")
        st.write("Connect to external APIs and cloud services for data integration.")
        st.page_link("pages/api_tools.py", label="API Integration", icon=":material/arrow_forward:")

with col5:
    with st.container(border=True):
        st.subheader(":material/settings: Settings")
        st.write("Configure API keys and app preferences.")
        st.page_link("pages/settings.py", label="Configure", icon=":material/arrow_forward:")

st.divider()




st.info("""
**Pro Tip:** All session data persists across pages. Upload data once and access it everywhere!
""", icon=":material/tips_and_updates:")
