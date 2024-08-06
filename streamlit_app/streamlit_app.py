import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Set page layout to wide
st.set_page_config(layout="wide")

with open("streamlit_app/assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Function to get Google Sheets client
def get_gsheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "streamlit_app/expense-tracker-412918-b05bae2e3dce.json", scope
    )
    client = gspread.authorize(creds)
    sheet = client.open("Expense Tracker Updated").sheet1
    return sheet


def save_to_gsheet(expenses):
    if "Date" in expenses.columns:
        expenses["Date"] = expenses["Date"].astype(str)
    else:
        st.error("'Date' column not found in the DataFrame.")
        return

    sheet = get_gsheet()

    # Get existing data
    existing_data = sheet.get_all_records()
    df_existing = pd.DataFrame(existing_data)

    if not df_existing.empty:
        # Append new data to existing data
        df_combined = pd.concat([df_existing, expenses], ignore_index=True)
    else:
        df_combined = expenses

    # Clear the existing content and update with combined data, including headers
    sheet.update([df_combined.columns.values.tolist()] + df_combined.values.tolist())


def add_expense():
    st.header("Add Expense")

    # Inputs for adding expenses
    date = st.date_input("Date", datetime.today())
    amount = st.number_input("Amount (INR)", min_value=0.0)
    description = st.text_input("Description")
    split_option = st.radio(
        "Choose Split Option", ["Equal", "Custom"], key="split_option"
    )

    # New input for "Paid By"
    paid_by = st.selectbox(
        "Paid By", [st.session_state["user1"], st.session_state["user2"]], key="paid_by"
    )

    if split_option == "Equal":
        user1_share = amount / 2
        user2_share = amount / 2
    else:
        user1_share = st.number_input(
            f"{st.session_state['user1']}'s Share (INR)",
            min_value=0.0,
            value=0.0,
            key="user1_share",
        )
        user2_share = st.number_input(
            f"{st.session_state['user2']}'s Share (INR)",
            min_value=0.0,
            value=0.0,
            key="user2_share",
        )

    # Category dropdown
    categories = ["Food", "Transport", "Entertainment", "Utilities", "Others"]
    category = st.selectbox("Category", categories, key="category")

    if st.button("Add Expense", key="add_expense"):
        if "expenses" not in st.session_state:
            st.session_state["expenses"] = []

        # Ensure total amount matches the sum of shares
        if amount != (user1_share + user2_share):
            st.error("Total amount must match the sum of shares.")
            return

        expense_entry = {
            "Date": date,
            "Amount (INR)": amount,
            "Description": description,
            f"{st.session_state['user1']}'s Share (INR)": user1_share,
            f"{st.session_state['user2']}'s Share (INR)": user2_share,
            "Category": category,
            "Paid By": paid_by,
        }
        st.session_state["expenses"].append(expense_entry)
        st.success("Expense added successfully!")

        # Save to Google Sheets
        df_new_entry = pd.DataFrame(st.session_state["expenses"])
        save_to_gsheet(df_new_entry)


def view_expense_history():
    st.header("Expense History")

    # Fetch the most recent data from Google Sheets
    sheet = get_gsheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty:
        # Convert 'Date' column to datetime format if not already
        df["Date"] = pd.to_datetime(df["Date"])
        start_date_default = df["Date"].min().date()  # Use min date from DataFrame
        end_date_default = df["Date"].max().date()  # Use max date from DataFrame

        # Extract unique months for month filter
        months = df["Date"].dt.to_period("M").drop_duplicates().sort_values()
        month_names = months.dt.strftime("%B %Y").tolist()
        month_map = {name: period for name, period in zip(month_names, months)}
        selected_month = st.selectbox(
            "Filter by Month", ["All"] + month_names, key="month_filter"
        )
    else:
        start_date_default = datetime.today().date()  # Default to today if empty
        end_date_default = datetime.today().date()  # Default to today if empty
        selected_month = "All"  # Default to "All" if empty

    # Custom date filter
    st.subheader("Filter by Date Range and Month")
    col1, col2 = st.columns([1, 1])
    with col1:
        start_date = st.date_input("Start Date", start_date_default, key="start_date")
    with col2:
        end_date = st.date_input("End Date", end_date_default, key="end_date")

    if st.button("Refresh", key="refresh_view_expense"):
        # Refresh data
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])  # Ensure date conversion
        mask = (df["Date"] >= pd.Timestamp(start_date)) & (
            df["Date"] <= pd.Timestamp(end_date)
        )

        if selected_month != "All":
            month_filter = month_map[selected_month]
            mask = mask & (df["Date"].dt.to_period("M") == month_filter)

        filtered_df = df.loc[mask]

        if filtered_df.empty:
            st.write("No expenses found for the selected date range or month.")
            return

        # Style the DataFrame
        styled_df = (
            filtered_df.style.set_properties(
                **{"border": "1px solid #ddd", "padding": "10px"}
            )
            .set_table_styles(
                [
                    {
                        "selector": "thead th",
                        "props": [
                            ("font-weight", "bold"),
                            ("border", "1px solid #ddd"),
                            ("text-align", "center"),
                        ],
                    },
                    {"selector": "tbody tr", "props": [("border", "1px solid #ddd")]},
                    {"selector": "tbody td", "props": [("border", "1px solid #ddd")]},
                ]
            )
            .format(
                {
                    "Amount (INR)": lambda x: f"₹{x:.2f}".rstrip("0").rstrip("."),
                    f"{st.session_state['user1']}'s Share (INR)": lambda x: f"₹{x:.2f}".rstrip(
                        "0"
                    ).rstrip(
                        "."
                    ),
                    f"{st.session_state['user2']}'s Share (INR)": lambda x: f"₹{x:.2f}".rstrip(
                        "0"
                    ).rstrip(
                        "."
                    ),
                }
            )
            .set_table_attributes(
                'style="width: 100%; margin: 0 auto; border-collapse: collapse;"'
            )
            .to_html()
        )

        st.markdown(styled_df, unsafe_allow_html=True)
    else:
        st.write("No expenses added yet.")


def calculate_owage():
    st.header("Owe Calculation")

    # Fetch the most recent data from Google Sheets
    sheet = get_gsheet()
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if not df.empty:
        # Convert 'Date' column to datetime format if not already
        df["Date"] = pd.to_datetime(df["Date"])
        start_date_default = df["Date"].min().date()  # Use min date from DataFrame
        end_date_default = df["Date"].max().date()  # Use max date from DataFrame

        # Extract unique months for month filter
        months = df["Date"].dt.to_period("M").drop_duplicates().sort_values()
        month_names = months.dt.strftime("%B %Y").tolist()
        month_map = {name: period for name, period in zip(month_names, months)}
        selected_month = st.selectbox(
            "Filter by Month", ["All"] + month_names, key="owage_month_filter"
        )
    else:
        start_date_default = datetime.today().date()  # Default to today if empty
        end_date_default = datetime.today().date()  # Default to today if empty
        selected_month = "All"  # Default to "All" if empty

    # Custom date filter
    st.subheader("Filter by Date Range and Month")
    col1, col2 = st.columns([1, 1])
    with col1:
        start_date = st.date_input(
            "Start Date", start_date_default, key="owage_start_date"
        )
    with col2:
        end_date = st.date_input("End Date", end_date_default, key="owage_end_date")

    if st.button("Calculate", key="calculate_owage"):
        # Refresh data
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        df["Date"] = pd.to_datetime(df["Date"])  # Ensure date conversion
        mask = (df["Date"] >= pd.Timestamp(start_date)) & (
            df["Date"] <= pd.Timestamp(end_date)
        )

        if selected_month != "All":
            month_filter = month_map[selected_month]
            mask = mask & (df["Date"].dt.to_period("M") == month_filter)

        filtered_df = df.loc[mask]

        if filtered_df.empty:
            st.write("No expenses found for the selected date range or month.")
            return

        # Calculate owage
        user1_owes = filtered_df[filtered_df["Paid By"] == st.session_state["user2"]][
            f"{st.session_state['user1']}'s Share (INR)"
        ].sum()
        user2_owes = filtered_df[filtered_df["Paid By"] == st.session_state["user1"]][
            f"{st.session_state['user2']}'s Share (INR)"
        ].sum()

        total_owage = user1_owes - user2_owes
        if total_owage < 0:
            st.write(
                f"{st.session_state['user2']} owes {st.session_state['user1']} ₹{abs(total_owage):.2f}"
            )
        elif total_owage > 0:
            st.write(
                f"{st.session_state['user1']} owes {st.session_state['user2']} ₹{abs(total_owage):.2f}"
            )
        else:
            st.write("No one owes anything")


def login():
    st.title("Login")

    # Check if already logged in
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return  # Exit if already logged in

    # Authentication form
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        with st.form(key="auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submit_button = st.form_submit_button("Authenticate")

            if submit_button:
                # Check credentials from secrets.toml
                if (
                    username == st.secrets["credentials"]["username"]
                    and password == st.secrets["credentials"]["password"]
                ):
                    st.session_state["authenticated"] = True
                    st.session_state["authenticated_user"] = username
                    st.success("Authentication successful! Please set user names.")
                    st.experimental_rerun()  # Refresh to show the next form
                else:
                    st.error("Invalid username or password.")
    else:
        # Prompt for user names after authentication
        if "user1" not in st.session_state or "user2" not in st.session_state:
            with st.form(key="user_form"):
                user1 = st.text_input("Enter name for User 1", key="user1_name")
                user2 = st.text_input("Enter name for User 2", key="user2_name")

                submit_button = st.form_submit_button("Set User Names")

                if submit_button:
                    if user1 and user2:
                        st.session_state["user1"] = user1
                        st.session_state["user2"] = user2
                        st.session_state["logged_in"] = True
                        st.session_state["show_login"] = False
                        st.session_state["authenticated"] = False
                        st.success("User names set successfully!")
                        st.experimental_rerun()  # Refresh to proceed to the main content
                    else:
                        st.error("Please enter both user names.")


def main():
    # Initialize session state if not already set
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Display login or main content based on login state
    if st.session_state["logged_in"]:
        st.title("Expense Tracker")

        tab1, tab2, tab3 = st.tabs(
            ["Add Expense", "View Expense History", "Owe Calculation"]
        )

        with tab1:
            add_expense()
        with tab2:
            view_expense_history()
        with tab3:
            calculate_owage()
    else:
        login()


if __name__ == "__main__":
    main()
