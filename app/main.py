import streamlit as st
import pandas as pd
import numpy as np
import os,sys


rpath = os.path.abspath('')
if rpath not in sys.path:
    sys.path.insert(0, rpath)

from app.utils import load_data


def detect_outliers_iqr(data):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = ((data < lower_bound) | (data > upper_bound)).sum()
    return outliers


def main():
    st.set_page_config(layout="wide")  # Set the page layout to wide

    st.title('MoonLigh Energy Solutions')

    # File uploader widget
    uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

    if uploaded_file is not None:
        # Load data from the uploaded CSV file
        data = load_data(uploaded_file)

        # Create a sidebar for navigation
        with st.sidebar:
            st.header('Navigation')
            view_option = st.radio('Select view option', 
                                   ['Head', 'Tail', 'Summary Statistics', 'Data Quality Check'])

        # Main dashboard layout
        col1, col2 = st.columns([2, 1])

        with col1:
            if view_option in ['Head', 'Tail']:
                # Slider for selecting the number of rows to display
                num_rows = st.slider('Number of rows to display', min_value=1, max_value=min(len(data), 100), value=5)
                
                if view_option == 'Head':
                    # Show the first few rows of the dataframe
                    st.subheader('Data Head')
                    st.dataframe(data.head(num_rows))
                elif view_option == 'Tail':
                    # Show the last few rows of the dataframe
                    st.subheader('Data Tail')
                    st.dataframe(data.tail(num_rows))
            
            elif view_option == 'Summary Statistics':
                # Calculate and display summary statistics for numeric columns
                st.subheader('Summary Statistics for Numeric Columns')
                numeric_data = data.select_dtypes(include='number')  # Select numeric columns only
                
                if not numeric_data.empty:
                    # Calculate summary statistics
                    summary = pd.DataFrame()
                    summary['Mean'] = numeric_data.mean()
                    summary['Median'] = numeric_data.median()
                    summary['Standard Deviation'] = numeric_data.std()
                    summary['Variance'] = numeric_data.var()
                    summary['Range'] = numeric_data.max() - numeric_data.min()
                    summary['Skewness'] = numeric_data.skew()
                    summary['25th Percentile'] = numeric_data.quantile(0.25)
                    summary['50th Percentile (Median)'] = numeric_data.quantile(0.50)
                    summary['75th Percentile'] = numeric_data.quantile(0.75)

                    # Rename index for clarity
                    summary.index.name = 'Column'
                    st.dataframe(summary)
                else:
                    st.write('No numeric columns found in the data.')

            elif view_option == 'Data Quality Check':
                # Check for missing values, incorrect entries, and outliers
                st.subheader('Data Quality Check Results')

                # Create subcolumns for displaying results
                with st.expander("Missing Values"):
                    missing_values = data.isnull().sum()
                    st.write(missing_values[missing_values > 0])

                with st.expander("Incorrect Entries (Negative Values)"):
                    columns_positive = ['GHI', 'DNI', 'DHI']
                    incorrect_entries = {}
                    for col in columns_positive:
                        if col in data.columns:
                            incorrect_entries[col] = (data[col] < 0).sum()
                    st.write(pd.Series(incorrect_entries))

                with st.expander("Outliers Detected (IQR Method)"):
                    columns_outliers = ['ModA', 'ModB', 'WS', 'WSgust']
                    outlier_results = {}
                    for col in columns_outliers:
                        if col in data.columns:
                            outlier_results[col] = detect_outliers_iqr(data[col])
                    st.write(pd.Series(outlier_results))
                    

        # Additional visual elements can be added here
        with col2:
            st.header('Dashboard Insights')

            # Example metrics
            if not data.empty:
                num_rows = len(data)
                num_columns = len(data.columns)
                st.metric("Total Rows", num_rows)
                st.metric("Total Columns", num_columns)

                # Example of a bar chart for numeric columns
                numeric_data = data.select_dtypes(include='number')
                if not numeric_data.empty:
                    st.bar_chart(numeric_data.mean())

        # Add footer
        st.markdown(
            """
            <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 0;
                width: 100%;
                text-align: center;
                padding: 10px;
                font-size: 3rem;
                display:flex;
                justify-content: center;
                align-items: center;
            }
            
            </style>
            <div class="footer">
                <p>Developer by Biruk Bizuayehu</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:
        st.write('Please upload a CSV file to see the data.')

if __name__ == "__main__":
    main()
