import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Define the scope and credentials for accessing Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "config/expense-tracker-412918-b05bae2e3dce.json", scope
)
client = gspread.authorize(credentials)

# Open the Google Sheet
spreadsheet = client.open("Expense Tracker Updated")
sheet = spreadsheet.sheet1


# Define a function to fetch data from Google Sheet
def fetch_expenses():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df


# Streamlit UI
st.title("View Expenses")

# Fetch and display expenses
df = fetch_expenses()

# Convert 'Date' column to datetime for filtering
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
df["Month_Year"] = df["Date"].dt.to_period("M")

# Create a list of months with names and year
months = df["Date"].apply(lambda x: x.strftime("%B %Y")).unique()
sorted_months = sorted(months, key=lambda x: datetime.strptime(x, "%B %Y"))

# Add an option to display all expenses
sorted_months.insert(0, "All")

# Dropdown for selecting month
selected_month = st.selectbox("Select Month", sorted_months)

# Filter data based on selected month
if selected_month == "All":
    filtered_df = df
else:
    selected_period = datetime.strptime(selected_month, "%B %Y").strftime("%Y-%m")
    filtered_df = df[df["Month_Year"] == pd.Period(selected_period, freq="M")]

# Display filtered data
st.dataframe(filtered_df, use_container_width=True)
