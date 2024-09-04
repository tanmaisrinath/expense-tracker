import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd
from datetime import datetime

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Define the scope and credentials for accessing Google Sheets
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["credentials"], scopes=scopes
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


st.title("View Expenses")

# Fetch and display expenses
df = fetch_expenses()

# Convert 'Date' column to datetime for filtering
df["Date"] = pd.to_datetime(df["Date"], format="%d-%m-%y")
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


# Drop the "Month_Year" column before displaying
filtered_df = filtered_df.drop(columns=["Month_Year"])

# Format the 'Date' column to remove the timestamp
filtered_df["Date"] = filtered_df["Date"].dt.strftime("%d-%m-%y")

# Calculate the total amount for the selected period
total_amount = filtered_df["Amount (INR)"].sum()

# Display filtered data without the index
st.dataframe(filtered_df, use_container_width=True)


st.write(f"Total Amount ({selected_month}): ₹{total_amount:,.2f}")

## Calulating Owage
tanmai_share = filtered_df.loc[
    filtered_df["Paid By"] == "Shivangi", "Tanmai's Share (INR)"
].sum()
shivangi_share = filtered_df.loc[
    filtered_df["Paid By"] == "Tanmai", "Shivangi's Share (INR)"
].sum()
st.write(f"Tanmai Owes Shivangi: **{tanmai_share}**")
st.write(f"Shivangi Owes Tanmai: **{shivangi_share}**")
