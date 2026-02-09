import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.title(":material/table_chart: Data Analysis")

st.markdown("Upload CSV or JSON files for instant analysis and insights.")

# File uploader
uploaded_file = st.file_uploader(
    "Upload your data file",
    type=["csv", "json"],
    help="Supported formats: CSV, JSON"
)

if uploaded_file is not None:
    # Store filename
    st.session_state.uploaded_filename = uploaded_file.name
    
    # Load data based on file type
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.json'):
            json_data = json.load(uploaded_file)
            # Try to convert to DataFrame
            if isinstance(json_data, list):
                df = pd.DataFrame(json_data)
            elif isinstance(json_data, dict):
                df = pd.DataFrame([json_data])
            else:
                st.error("JSON format not supported. Please use list of objects or single object.")
                st.stop()
        
        st.session_state.df = df
        st.success(f"✓ Loaded {len(df)} rows from {uploaded_file.name}", icon=":material/check_circle:")
        
    except Exception as e:
        st.error(f"Error loading file: {str(e)}", icon=":material/error:")
        st.stop()

# Display data if available
if st.session_state.df is not None:
    df = st.session_state.df
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        ":material/preview: Preview",
        ":material/analytics: Statistics",
        ":material/search: Explore",
        ":material/download: Export"
    ])
    
    with tab1:
        st.subheader("Data Preview")
        st.dataframe(
            df.head(100),
            use_container_width=True,
            height=400
        )
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", len(df))
        col2.metric("Columns", len(df.columns))
        col3.metric("Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        col4.metric("Null Values", df.isnull().sum().sum())
    
    with tab2:
        st.subheader("Statistical Summary")
        
        # Numeric columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            st.markdown("**Numeric Columns**")
            st.dataframe(
                df[numeric_cols].describe(),
                use_container_width=True
            )
        
        # Categorical columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        if len(categorical_cols) > 0:
            st.markdown("**Categorical Columns**")
            for col in categorical_cols[:5]:  # Show first 5
                with st.expander(f"Column: {col}"):
                    value_counts = df[col].value_counts().head(10)
                    st.bar_chart(value_counts)
                    st.caption(f"Top 10 values out of {df[col].nunique()} unique values")
        
        # Missing data analysis
        st.markdown("**Missing Data Analysis**")
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        if len(missing_data) > 0:
            missing_df = pd.DataFrame({
                'Column': missing_data.index,
                'Missing Count': missing_data.values,
                'Percentage': (missing_data.values / len(df) * 100).round(2)
            })
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.success("No missing data found!", icon=":material/check_circle:")
    
    with tab3:
        st.subheader("Data Explorer")
        
        # Column selector
        selected_cols = st.multiselect(
            "Select columns to display",
            df.columns.tolist(),
            default=df.columns.tolist()[:5]
        )
        
        if selected_cols:
            # Filter options
            col1, col2 = st.columns(2)
            
            with col1:
                filter_col = st.selectbox(
                    "Filter by column",
                    ["None"] + df.columns.tolist()
                )
            
            filtered_df = df[selected_cols].copy()
            
            if filter_col != "None":
                with col2:
                    if df[filter_col].dtype in ['object', 'category']:
                        unique_vals = df[filter_col].unique()
                        filter_val = st.multiselect(
                            f"Select {filter_col} values",
                            unique_vals
                        )
                        if filter_val:
                            filtered_df = df[df[filter_col].isin(filter_val)][selected_cols]
                    else:
                        min_val = float(df[filter_col].min())
                        max_val = float(df[filter_col].max())
                        filter_range = st.slider(
                            f"Filter {filter_col} range",
                            min_val, max_val,
                            (min_val, max_val)
                        )
                        filtered_df = df[
                            (df[filter_col] >= filter_range[0]) &
                            (df[filter_col] <= filter_range[1])
                        ][selected_cols]
            
            st.dataframe(filtered_df, use_container_width=True, height=400)
            st.caption(f"Showing {len(filtered_df)} of {len(df)} rows")
    
    with tab4:
        st.subheader("Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV export
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            csv = df.to_csv(index=False)
            
            st.download_button(
                label=":material/download: Download as CSV",
                data=csv,
                file_name=f"export_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # JSON export
            json_str = df.to_json(orient='records', indent=2)
            
            st.download_button(
                label=":material/download: Download as JSON",
                data=json_str,
                file_name=f"export_{timestamp}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # Excel export (if openpyxl available)
        try:
            import io
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
                
                # Add statistics sheet
                if len(numeric_cols) > 0:
                    df[numeric_cols].describe().to_excel(writer, sheet_name='Statistics')
            
            st.download_button(
                label=":material/download: Download as Excel",
                data=output.getvalue(),
                file_name=f"export_{timestamp}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        except ImportError:
            st.info("Install openpyxl to enable Excel export: `pip install openpyxl`")

else:
    # Show placeholder when no data
    st.info("Upload a CSV or JSON file to get started!", icon=":material/upload:")
    
    with st.expander("Example Data Format"):
        st.markdown("**CSV Example:**")
        st.code("""
name,age,city,score
Alice,28,New York,95
Bob,34,San Francisco,87
Charlie,23,Boston,92
        """)
        
        st.markdown("**JSON Example:**")
        st.code("""
[
  {"name": "Alice", "age": 28, "city": "New York", "score": 95},
  {"name": "Bob", "age": 34, "city": "San Francisco", "score": 87},
  {"name": "Charlie", "age": 23, "city": "Boston", "score": 92}
]
        """)
