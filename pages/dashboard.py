import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title(":material/bar_chart: Interactive Dashboard")

if st.session_state.df is not None:
    df = st.session_state.df
    
    st.success(f"Visualizing data from: {st.session_state.uploaded_filename}", icon=":material/check_circle:")
    
    # Get numeric and categorical columns
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # Chart type selector
    chart_type = st.selectbox(
        "Select Chart Type",
        ["Bar Chart", "Line Chart", "Scatter Plot", "Box Plot", "Histogram", "Pie Chart", "Heatmap"]
    )
    
    st.divider()
    
    if chart_type == "Bar Chart":
        col1, col2, col3 = st.columns(3)
        with col1:
            x_col = st.selectbox("X-axis", df.columns.tolist(), key="bar_x")
        with col2:
            y_col = st.selectbox("Y-axis", numeric_cols, key="bar_y") if numeric_cols else st.selectbox("Y-axis", df.columns.tolist())
        with col3:
            color_col = st.selectbox("Color by", ["None"] + categorical_cols, key="bar_color")
        
        if color_col == "None":
            fig = px.bar(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
        else:
            fig = px.bar(df, x=x_col, y=y_col, color=color_col, title=f"{y_col} by {x_col}")
        
        fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Line Chart":
        col1, col2, col3 = st.columns(3)
        with col1:
            x_col = st.selectbox("X-axis", df.columns.tolist(), key="line_x")
        with col2:
            y_cols = st.multiselect("Y-axis (can select multiple)", numeric_cols, default=numeric_cols[:1] if numeric_cols else [])
        with col3:
            color_col = st.selectbox("Color by", ["None"] + categorical_cols, key="line_color")
        
        if y_cols:
            if color_col == "None":
                fig = px.line(df, x=x_col, y=y_cols, title="Line Chart")
            else:
                fig = px.line(df, x=x_col, y=y_cols[0], color=color_col, title="Line Chart")
            
            fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Scatter Plot":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            x_col = st.selectbox("X-axis", numeric_cols, key="scatter_x") if numeric_cols else st.selectbox("X-axis", df.columns.tolist())
        with col2:
            y_col = st.selectbox("Y-axis", numeric_cols, key="scatter_y") if numeric_cols else st.selectbox("Y-axis", df.columns.tolist())
        with col3:
            color_col = st.selectbox("Color by", ["None"] + categorical_cols, key="scatter_color")
        with col4:
            size_col = st.selectbox("Size by", ["None"] + numeric_cols, key="scatter_size")
        
        kwargs = {"x": x_col, "y": y_col, "title": f"{y_col} vs {x_col}"}
        if color_col != "None":
            kwargs["color"] = color_col
        if size_col != "None":
            kwargs["size"] = size_col
        
        fig = px.scatter(df, **kwargs)
        fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Box Plot":
        col1, col2, col3 = st.columns(3)
        with col1:
            y_col = st.selectbox("Value", numeric_cols, key="box_y") if numeric_cols else st.selectbox("Value", df.columns.tolist())
        with col2:
            x_col = st.selectbox("Group by", ["None"] + categorical_cols, key="box_x")
        with col3:
            color_col = st.selectbox("Color by", ["None"] + categorical_cols, key="box_color")
        
        kwargs = {"y": y_col, "title": f"Distribution of {y_col}"}
        if x_col != "None":
            kwargs["x"] = x_col
        if color_col != "None":
            kwargs["color"] = color_col
        
        fig = px.box(df, **kwargs)
        fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Histogram":
        col1, col2, col3 = st.columns(3)
        with col1:
            x_col = st.selectbox("Column", numeric_cols, key="hist_x") if numeric_cols else st.selectbox("Column", df.columns.tolist())
        with col2:
            bins = st.slider("Number of bins", 5, 100, 30)
        with col3:
            color_col = st.selectbox("Color by", ["None"] + categorical_cols, key="hist_color")
        
        kwargs = {"x": x_col, "nbins": bins, "title": f"Distribution of {x_col}"}
        if color_col != "None":
            kwargs["color"] = color_col
        
        fig = px.histogram(df, **kwargs)
        fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "Pie Chart":
        if categorical_cols:
            col1, col2 = st.columns(2)
            with col1:
                names_col = st.selectbox("Categories", categorical_cols, key="pie_names")
            with col2:
                values_col = st.selectbox("Values", ["Count"] + numeric_cols, key="pie_values")
            
            if values_col == "Count":
                pie_data = df[names_col].value_counts().reset_index()
                pie_data.columns = [names_col, 'count']
                fig = px.pie(pie_data, names=names_col, values='count', title=f"Distribution of {names_col}")
            else:
                fig = px.pie(df, names=names_col, values=values_col, title=f"{values_col} by {names_col}")
            
            fig.update_layout(margin=dict(t=40, l=0, r=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No categorical columns available for pie chart")
    
    elif chart_type == "Heatmap":
        if len(numeric_cols) >= 2:
            # Correlation heatmap
            corr_matrix = df[numeric_cols].corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmid=0,
                text=corr_matrix.values.round(2),
                texttemplate='%{text}',
                textfont={"size": 10},
            ))
            
            fig.update_layout(
                title="Correlation Heatmap",
                margin=dict(t=40, l=0, r=0, b=0),
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Need at least 2 numeric columns for heatmap")
    
    # Summary statistics section
    st.divider()
    st.subheader(":material/analytics: Quick Statistics")
    
    cols = st.columns(4)
    
    if numeric_cols:
        for i, col in enumerate(numeric_cols[:4]):
            with cols[i % 4]:
                st.metric(
                    label=col,
                    value=f"{df[col].mean():.2f}",
                    delta=f"σ={df[col].std():.2f}"
                )

else:
    st.info("Upload data in the Data Analysis page first!", icon=":material/info:")
    st.page_link("pages/data_analysis.py", label="Go to Data Analysis", icon=":material/arrow_forward:")
    
    # Show sample visualization
    st.subheader("Sample Dashboard")
    st.caption("This is what your dashboard will look like with data")
    
    sample_df = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Sales': [120, 150, 180, 160, 200, 220],
        'Customers': [50, 60, 75, 70, 85, 95],
        'Category': ['A', 'B', 'A', 'B', 'A', 'B']
    })
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(sample_df, x='Month', y='Sales', color='Category', title='Sample Bar Chart')
        fig1.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.line(sample_df, x='Month', y='Customers', title='Sample Line Chart')
        fig2.update_layout(margin=dict(t=40, l=0, r=0, b=0))
        st.plotly_chart(fig2, use_container_width=True)
