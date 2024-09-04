import streamlit as st

with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Function to check credentials
def check_credentials(username, password):
    stored_username = st.secrets["credentials"]["username"]
    stored_password = st.secrets["credentials"]["password"]
    return username == stored_username and password == stored_password

# Function to display the login page
def show_login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if check_credentials(username, password):
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()  # Reload the app to show the authenticated content
        else:
            st.error("Invalid username or password")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Check if user is logged in
if not st.session_state.logged_in:
    # Display login page
    show_login_page()
else:
      

    # Define pages
    home_page = st.Page(
        page="views/home_page.py", title="Home", icon=":material/home:", default=True
    )
    add_expense_page = st.Page(
        page="views/add_expense.py", title="Add Expense", icon=":material/add:"
    )
    view_expenses_page = st.Page(
        page="views/view_expenses.py", title="View Expenses", icon=":material/visibility:"
    )

    # Navigation
    pg = st.navigation(pages=[home_page, add_expense_page, view_expenses_page])
    pg.run()
