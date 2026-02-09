import streamlit as st
import requests
import json
import pandas as pd

st.title(":material/cloud: API Tools")

st.markdown("Connect to external APIs and cloud services for data integration.")

# API type selector
api_type = st.selectbox(
    "Select API Type",
    ["REST API", "GraphQL", "Custom Request"],
    help="Choose the type of API you want to connect to"
)

st.divider()

if api_type == "REST API":
    st.subheader("REST API Client")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        url = st.text_input(
            "API Endpoint URL",
            placeholder="https://api.example.com/data",
            help="Enter the full URL of the API endpoint"
        )
    
    with col2:
        method = st.selectbox("Method", ["GET", "POST", "PUT", "DELETE"])
    
    # Headers
    with st.expander("Headers (Optional)", expanded=False):
        headers_text = st.text_area(
            "Enter headers as JSON",
            value='{\n  "Content-Type": "application/json"\n}',
            height=100
        )
    
    # Request body (for POST/PUT)
    if method in ["POST", "PUT"]:
        with st.expander("Request Body", expanded=True):
            body_text = st.text_area(
                "Enter request body as JSON",
                value='{\n  "key": "value"\n}',
                height=150
            )
    
    # Authentication
    with st.expander("Authentication (Optional)", expanded=False):
        auth_type = st.selectbox("Auth Type", ["None", "Bearer Token", "API Key", "Basic Auth"])
        
        if auth_type == "Bearer Token":
            token = st.text_input("Token", type="password")
        elif auth_type == "API Key":
            api_key_name = st.text_input("Key Name", value="X-API-Key")
            api_key_value = st.text_input("Key Value", type="password")
        elif auth_type == "Basic Auth":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
    
    if st.button(":material/send: Send Request", type="primary", use_container_width=True):
        if not url:
            st.error("Please enter a URL", icon=":material/error:")
        else:
            try:
                # Prepare headers
                headers = json.loads(headers_text) if headers_text else {}
                
                # Add authentication
                if auth_type == "Bearer Token":
                    headers["Authorization"] = f"Bearer {token}"
                elif auth_type == "API Key":
                    headers[api_key_name] = api_key_value
                
                auth = None
                if auth_type == "Basic Auth":
                    auth = (username, password)
                
                # Prepare body
                body = None
                if method in ["POST", "PUT"] and body_text:
                    body = json.loads(body_text)
                
                # Make request
                with st.spinner("Sending request..."):
                    if method == "GET":
                        response = requests.get(url, headers=headers, auth=auth, timeout=30)
                    elif method == "POST":
                        response = requests.post(url, headers=headers, json=body, auth=auth, timeout=30)
                    elif method == "PUT":
                        response = requests.put(url, headers=headers, json=body, auth=auth, timeout=30)
                    elif method == "DELETE":
                        response = requests.delete(url, headers=headers, auth=auth, timeout=30)
                
                # Display results
                st.success(f"Response: {response.status_code} {response.reason}", icon=":material/check_circle:")
                
                # Response tabs
                tab1, tab2, tab3 = st.tabs([":material/code: Response", ":material/table_chart: Data View", ":material/info: Headers"])
                
                with tab1:
                    try:
                        json_response = response.json()
                        st.json(json_response)
                        
                        # Store in session state
                        st.session_state.api_data = json_response
                    except:
                        st.code(response.text)
                
                with tab2:
                    try:
                        json_response = response.json()
                        if isinstance(json_response, list):
                            df = pd.DataFrame(json_response)
                            st.dataframe(df, use_container_width=True)
                            
                            # Option to save to session
                            if st.button("Save to Session", key="save_api_data"):
                                st.session_state.df = df
                                st.session_state.uploaded_filename = "API Response"
                                st.success("Data saved! View in Data Analysis or Dashboard")
                        elif isinstance(json_response, dict):
                            df = pd.DataFrame([json_response])
                            st.dataframe(df, use_container_width=True)
                    except:
                        st.info("Response is not JSON or cannot be converted to DataFrame")
                
                with tab3:
                    st.json(dict(response.headers))
                
            except requests.exceptions.Timeout:
                st.error("Request timed out", icon=":material/error:")
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {str(e)}", icon=":material/error:")
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {str(e)}", icon=":material/error:")

elif api_type == "GraphQL":
    st.subheader("GraphQL Client")
    
    url = st.text_input(
        "GraphQL Endpoint",
        placeholder="https://api.example.com/graphql"
    )
    
    query = st.text_area(
        "GraphQL Query",
        value="""query {
  users {
    id
    name
    email
  }
}""",
        height=200
    )
    
    with st.expander("Variables (Optional)", expanded=False):
        variables = st.text_area(
            "Variables as JSON",
            value='{}',
            height=100
        )
    
    with st.expander("Headers (Optional)", expanded=False):
        headers_text = st.text_area(
            "Headers as JSON",
            value='{\n  "Content-Type": "application/json"\n}',
            height=100
        )
    
    if st.button(":material/send: Execute Query", type="primary", use_container_width=True):
        if not url or not query:
            st.error("Please enter both URL and query", icon=":material/error:")
        else:
            try:
                headers = json.loads(headers_text) if headers_text else {}
                vars_dict = json.loads(variables) if variables else {}
                
                payload = {
                    "query": query,
                    "variables": vars_dict
                }
                
                with st.spinner("Executing query..."):
                    response = requests.post(url, json=payload, headers=headers, timeout=30)
                
                st.success(f"Response: {response.status_code}", icon=":material/check_circle:")
                
                json_response = response.json()
                st.json(json_response)
                
                # Try to extract data
                if "data" in json_response:
                    st.session_state.api_data = json_response["data"]
                
            except Exception as e:
                st.error(f"Error: {str(e)}", icon=":material/error:")

elif api_type == "Custom Request":
    st.subheader("Custom HTTP Request")
    
    st.markdown("""
    Build a custom HTTP request with full control over all parameters.
    """)
    
    url = st.text_input("URL", placeholder="https://api.example.com/endpoint")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        method = st.text_input("Method", value="GET")
    with col2:
        timeout = st.number_input("Timeout (seconds)", min_value=1, max_value=300, value=30)
    with col3:
        allow_redirects = st.checkbox("Allow Redirects", value=True)
    
    headers_text = st.text_area("Headers (JSON)", value='{}', height=100)
    params_text = st.text_area("Query Parameters (JSON)", value='{}', height=100)
    body_text = st.text_area("Body (JSON)", value='{}', height=150)
    
    if st.button(":material/send: Send Custom Request", type="primary"):
        try:
            headers = json.loads(headers_text)
            params = json.loads(params_text)
            body = json.loads(body_text) if body_text.strip() != '{}' else None
            
            with st.spinner("Sending..."):
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=body,
                    timeout=timeout,
                    allow_redirects=allow_redirects
                )
            
            st.success(f"Status: {response.status_code}", icon=":material/check_circle:")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Status Code", response.status_code)
            with col2:
                st.metric("Response Time", f"{response.elapsed.total_seconds():.3f}s")
            
            try:
                st.json(response.json())
            except:
                st.code(response.text)
                
        except Exception as e:
            st.error(f"Error: {str(e)}", icon=":material/error:")

st.divider()

# Popular APIs section
with st.expander(":material/lightbulb: Popular Public APIs", expanded=False):
    st.markdown("""
    ### Free APIs to Try
    
    **JSONPlaceholder** (Fake REST API)
    - URL: `https://jsonplaceholder.typicode.com/users`
    - Method: GET
    - No auth required
    
    **CoinGecko** (Crypto prices)
    - URL: `https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd`
    - Method: GET
    - No auth required
    
    **OpenWeatherMap** (Weather data)
    - URL: `https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY`
    - Method: GET
    - Requires free API key
    
    **GitHub API** (Repository data)
    - URL: `https://api.github.com/users/octocat`
    - Method: GET
    - No auth required (rate limited)
    """)
