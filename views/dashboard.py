import streamlit as st
import gspread
from google.oauth2 import service_account
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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


def main():
    # Streamlit UI
    st.title("Expense Dashboard")

    # Fetch and display expenses
    df = fetch_expenses()

    # Convert 'Date' column to datetime for filtering
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Month_Year"] = df["Date"].dt.to_period("M")
    df["Day"] = df["Date"].dt.day
    df["Year"] = df["Date"].dt.year

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_year = st.sidebar.selectbox(
        "Select Year", sorted(df["Year"].unique(), reverse=True)
    )
    selected_month = st.sidebar.selectbox(
        "Select Month", sorted(df["Date"].dt.to_period("M").unique(), reverse=True)
    )
    selected_category = st.sidebar.multiselect(
        "Select Category", df["Category"].unique()
    )

    # Filter data based on sidebar inputs
    filtered_df = df[
        (df["Year"] == selected_year)
        & (df["Month_Year"] == selected_month)
        & (df["Category"].isin(selected_category) if selected_category else True)
    ]

    # Display summary statistics
    st.header("Summary Statistics")
    st.write(f"Total Expenses: ₹{filtered_df['Amount (INR)'].sum():,.2f}")
    st.write(f"Number of Transactions: {filtered_df.shape[0]}")

    # Visualizations
    st.header("Visualizations")

    # 1. Expenses by Category
    st.subheader("Expenses by Category")
    category_expenses = (
        filtered_df.groupby("Category")["Amount (INR)"].sum().reset_index()
    )
    st.bar_chart(category_expenses.set_index("Category"))

    # 2. Expenses by Month
    st.subheader("Expenses by Month")
    monthly_expenses = (
        df.groupby(df["Date"].dt.to_period("M"))["Amount (INR)"].sum().reset_index()
    )
    monthly_expenses["Date"] = monthly_expenses["Date"].dt.to_timestamp()
    st.line_chart(monthly_expenses.set_index("Date"))

    # 3. Daily Expenses Histogram
    st.subheader("Daily Expenses Distribution")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df["Day"], kde=True, ax=ax)
    ax.set_xlabel("Day of the Month")
    ax.set_ylabel("Frequency")
    ax.set_title("Distribution of Expenses by Day")
    st.pyplot(fig)

    # 4. Pie Chart of Expenses by Category
    st.subheader("Expense Distribution by Category")
    fig, ax = plt.subplots()
    category_distribution = filtered_df.groupby("Category")["Amount (INR)"].sum()
    ax.pie(
        category_distribution,
        labels=category_distribution.index,
        autopct="%1.1f%%",
        startangle=140,
    )
    ax.set_title("Expense Distribution by Category")
    st.pyplot(fig)
