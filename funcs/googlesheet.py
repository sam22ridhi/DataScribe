import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

def get_google_sheet_data(sheet_id, range_name):
    creds = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
    )
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get("values", [])
    return pd.DataFrame(values[1:], columns=values[0])

def update_google_sheet(sheet_id, range_name, data):
    try:
        # Define the Google Sheets API scope
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
        client = gspread.authorize(creds)

        # Open the Google Sheet and specify the worksheet
        sheet = client.open_by_key(sheet_id).worksheet(range_name.split("!")[0])

        # Prepare data for update
        data_to_update = [data.columns.tolist()] + data.values.tolist()

        # Clear the existing content in the specified range and update it with new data
        sheet.clear()
        sheet.update(range_name, data_to_update)

        st.success("Data successfully updated in the Google Sheet!")
    except Exception as e:
        st.error(f"Error updating Google Sheet: {e}")