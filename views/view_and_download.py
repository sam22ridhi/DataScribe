import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def CreatePage():
    st.header("View & Download Results")

    if "results" in st.session_state and st.session_state["results"]:
        results_df = pd.DataFrame(st.session_state["results"])
        st.write("### Results Preview")

        # Display the results preview
        if "Extracted Information" in results_df.columns and "Search Results" in results_df.columns:
            st.dataframe(results_df.style.map(lambda val: 'background-color: #d3f4ff' if isinstance(val, str) else '', subset=["Extracted Information", "Search Results"]))
        else:
            st.warning("Required columns are missing in results data.")

        # Download options
        download_option = st.selectbox(
            "Select data to download:",
            ["All Results", "Extracted Information", "Web Results"]
        )

        if download_option == "All Results":
            data_to_download = results_df
        elif download_option == "Extracted Information":
            data_to_download = results_df[["Entity", "Extracted Information"]]
        elif download_option == "Web Results":
            data_to_download = results_df[["Entity", "Search Results"]]

        st.download_button(
            label=f"Download {download_option} as CSV",
            data=data_to_download.to_csv(index=False),
            file_name=f"{download_option.lower().replace(' ', '_')}.csv",
            mime="text/csv"
        )

        # Option to update Google Sheets
        update_option = st.selectbox(
            "Do you want to update Google Sheets?",
            ["No", "Yes"]
        )

        if update_option == "Yes":
            if 'sheet_id' not in st.session_state:
                st.session_state.sheet_id = ''
            if 'range_name' not in st.session_state:
                st.session_state.range_name = ''

            # Input fields for Google Sheets ID and Range
            sheet_id = st.text_input("Enter Google Sheet ID", value=st.session_state.sheet_id)
            range_name = st.text_input("Enter Range (e.g., 'Sheet1!A1')", value=st.session_state.range_name)

            if sheet_id and range_name:
                st.session_state.sheet_id = sheet_id
                st.session_state.range_name = range_name

                # Prepare data for update
                data_to_update = [results_df.columns.tolist()] + results_df.values.tolist()

                # Update Google Sheets button
                if st.button("Update Google Sheet"):
                    try:
                        if '!' not in range_name:
                            st.error("Invalid range format. Please use the format 'SheetName!Range'.")
                        else:
                            sheet_name, cell_range = range_name.split('!', 1) 
                            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
                            creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
                            client = gspread.authorize(creds)
                            sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
                            sheet.clear()
                            sheet.update(f"{cell_range}", data_to_update)
                            st.success("Data updated in the Google Sheet!")
                    except Exception as e:
                        st.error(f"Error updating Google Sheet: {e}")
            else:
                st.warning("Please enter both the Sheet ID and Range name before updating.")
    else:
        st.warning("No results available to view. Please run the extraction process.")