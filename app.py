import streamlit as st

# Page config - must be first Streamlit command
st.set_page_config(
    page_title="AI Data Analytics Dashboard",
    page_icon=":material/rocket:",
    layout="wide"
)

# Initialize session state BEFORE navigation
st.session_state.setdefault("messages", [])
st.session_state.setdefault("df", None)
st.session_state.setdefault("uploaded_filename", None)
st.session_state.setdefault("api_data", None)
st.session_state.setdefault("llm_provider", "OpenAI")
st.session_state.setdefault("analysis_results", {})

# Define pages with Material icons
page_home = st.Page("pages/home.py", title="Home", icon=":material/home:")
page_chat = st.Page("pages/chatbot.py", title="AI Chatbot", icon=":material/chat:")
page_data = st.Page("pages/data_analysis.py", title="Data Analysis", icon=":material/table_chart:")
page_dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/bar_chart:")
page_api = st.Page("pages/api_tools.py", title="API Tools", icon=":material/cloud:")
page_settings = st.Page("pages/settings.py", title="Settings", icon=":material/settings:")

# Navigation with top bar layout
pg = st.navigation(
    {
        "": [page_home, page_chat, page_data, page_dashboard, page_api],
        "Config": [page_settings],
    },
    position="top"
)

pg.run()