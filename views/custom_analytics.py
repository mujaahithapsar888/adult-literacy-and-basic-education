import streamlit as st
import pandas as pd
import plotly.express as px

def render_custom_analytics():
    st.title("📊 Custom Dataset Analysis")
    st.markdown("Upload your own dataset (CSV or Excel) to instantly visualize and analyze the data.")
    
    uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"])
    
    if uploaded_file is not None:
        try:
            # Read the dataset
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                
            st.success("File uploaded successfully!")
            
            # Show dataset preview and metrics
            st.subheader("Data Preview")
            col1, col2 = st.columns(2)
            col1.metric("Total Rows", df.shape[0])
            col2.metric("Total Columns", df.shape[1])
            
            st.dataframe(df.head(100), use_container_width=True)
            
            st.markdown("---")
            
            # Interactive Chart Builder
            st.subheader("📈 Build Interactive Chart")
            
            chart_col1, chart_col2, chart_col3 = st.columns(3)
            
            with chart_col1:
                chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Pie Chart"])
            
            with chart_col2:
                # Select X-axis (all columns)
                x_col = st.selectbox("X-Axis", df.columns.tolist())
                
            with chart_col3:
                # Select Y-axis (prefer numeric columns, but allow all)
                numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
                y_options = numeric_cols if numeric_cols else df.columns.tolist()
                y_col = st.selectbox("Y-Axis / Values", y_options)
                
            # Generate Chart button
            if st.button("Generate Chart", type="primary"):
                try:
                    if chart_type == "Bar Chart":
                        fig = px.bar(df, x=x_col, y=y_col, color=x_col if len(df[x_col].unique()) < 20 else None)
                    elif chart_type == "Line Chart":
                        fig = px.line(df, x=x_col, y=y_col, markers=True)
                    elif chart_type == "Scatter Plot":
                        fig = px.scatter(df, x=x_col, y=y_col, color=x_col if len(df[x_col].unique()) < 20 else None)
                    elif chart_type == "Pie Chart":
                        # For pie charts, group by the category (x_col) and sum the values (y_col)
                        pie_data = df.groupby(x_col, as_index=False)[y_col].sum()
                        fig = px.pie(pie_data, names=x_col, values=y_col, hole=0.4)
                    
                    fig.update_layout(height=500, margin=dict(l=20, r=20, t=30, b=20))
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Could not generate chart: {e}")
                    
        except Exception as e:
            st.error(f"Error reading the file: {e}")
    else:
        st.info("Awaiting file upload. Please upload a CSV or Excel file to get started.")
