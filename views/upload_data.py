import streamlit as st
from funcs.googlesheet import get_google_sheet_data
import pandas as pd

def CreatePage():   

    st.header("Upload or Connect Your Data")
    data_source = st.radio("Choose data source:", ["CSV Files", "Google Sheets"])

    if data_source == "CSV Files":
        if "data" in st.session_state:
            st.success("Data uploaded successfully! Here is a preview:")
            st.dataframe(st.session_state["data"].head(10))  # Display only the first 10 rows for a cleaner view
        else:
            uploaded_files = st.file_uploader("Upload your CSV files", type=["csv"], accept_multiple_files=True)

            if uploaded_files is not None:
                dfs = []
                for uploaded_file in uploaded_files:
                    try:
                        df = pd.read_csv(uploaded_file)
                        dfs.append(df)
                    except Exception as e:
                        st.error(f"Error reading file {uploaded_file.name}: {e}")
                
                if dfs:
                    full_data = pd.concat(dfs, ignore_index=True)
                    st.session_state["data"] = full_data
                    st.success("Data uploaded successfully! Here is a preview:")
                    st.dataframe(full_data.head(10))  # Show preview of first 10 rows
                else:
                    st.warning("No valid data found in the uploaded files.")
            
            if st.button("Clear Data"):
                del st.session_state["data"]
                st.success("Data has been cleared!")

    elif data_source == "Google Sheets":
        sheet_id = st.text_input("Enter Google Sheet ID")
        range_name = st.text_input("Enter the data range (e.g., Sheet1!A1:C100)")

        if sheet_id and range_name:
            if st.button("Fetch Data"):
                with st.spinner("Fetching data from Google Sheets..."):
                    try:
                        data = get_google_sheet_data(sheet_id, range_name)
                        st.session_state["data"] = data
                        st.success("Data fetched successfully! Here is a preview:")
                        st.dataframe(data.head(10))  # Show preview of first 10 rows
                    except Exception as e:
                        st.error(f"Error fetching data: {e}")
        else:
            st.warning("Please enter both Sheet ID and Range name before fetching data.")

