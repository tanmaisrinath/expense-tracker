import streamlit as st
import gspread
from google.oauth2 import service_account
from datetime import datetime
import time

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


# Define a function to add data to Google Sheet
def add_expense(date, amount, description, split_type, paid_by, category):
    if split_type == "Equal":
        amount1 = amount / 2
        amount2 = amount / 2
    else:  # Custom split
        amount1 = st.session_state.custom_split_amount1
        amount2 = st.session_state.custom_split_amount2

    # Prepare the data to be appended
    data = [
        date.strftime("%Y-%m-%d"),
        description,
        amount,
        paid_by,
        amount1,
        amount2,
        category,
    ]

    # Append data to Google Sheet
    sheet.append_row(data)


def run():
    # Streamlit UI
    st.title("Add Expense")

    # Initialize session state variables
    if "custom_split_amount1" not in st.session_state:
        st.session_state.custom_split_amount1 = 0.0
    if "custom_split_amount2" not in st.session_state:
        st.session_state.custom_split_amount2 = 0.0
    if "split_type" not in st.session_state:
        st.session_state.split_type = "Equal"

    # Input form
    with st.form("expense_form"):
        date = st.date_input("Date", datetime.today())
        amount = st.number_input("Amount (INR)", min_value=0.0, format="%.2f")
        description = st.text_input(
            "Description", placeholder="What did you blow your money on?"
        )

        # Dropdown for category
        category = st.selectbox("Category", ["Food", "Transport", "Events", "Others"])

        # Define split options
        split_options = ["Equal", "Custom"]

        # Radio button for payment split
        split_type = st.radio(
            "Payment Split",
            split_options,
            index=split_options.index(st.session_state.split_type),
        )

        # Update session state with the selected split type
        st.session_state.split_type = split_type

        # Always show custom split fields
        st.session_state.custom_split_amount1 = st.number_input(
            f"{st.session_state.user1}'s Share",
            min_value=0.0,
            format="%.2f",
            value=st.session_state.custom_split_amount1,
        )
        st.session_state.custom_split_amount2 = st.number_input(
            f"{st.session_state.user2}'s Share",
            min_value=0.0,
            format="%.2f",
            value=st.session_state.custom_split_amount2,
        )

        # Set equal split amounts if "Equal" is selected
        if split_type == "Equal":
            st.session_state.custom_split_amount1 = amount / 2
            st.session_state.custom_split_amount2 = amount / 2

        # Dropdown for who paid
        paid_by = st.selectbox("Paid By", [st.session_state.user1, st.session_state.user2])

        # Submit button inside the form
        submit_button = st.form_submit_button("Submit")

        # Validation and data handling
        if submit_button:
            if not description.strip():
                st.error("Description is required.")
            elif amount <= 0:
                st.error("Amount must be greater than 0.")
            elif split_type == "Custom" and (
                st.session_state.custom_split_amount1 <= 0
                or st.session_state.custom_split_amount2 <= 0
            ):
                st.error("Custom split amounts must be greater than 0.")
            else:
                add_expense(date, amount, description, split_type, paid_by, category)
                st.success("Expense added successfully!")

                st.session_state.date = datetime.today()
                st.session_state.amount = 0.0
                st.session_state.description = ""
                st.session_state.category = "Food"
                st.session_state.split_type = "Equal"
                st.session_state.custom_split_amount1 = 0.0
                st.session_state.custom_split_amount2 = 0.0
                st.session_state.paid_by = st.session_state.user1

                # Display a progress bar for loading
                time.sleep(1.5)

                # Trigger a re-run to reflect changes immediately
                st.rerun()
