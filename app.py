import streamlit as st

# Set up the page configuration with default layout
st.set_page_config(page_title="TickTrack2")

home_page = st.Page(
    page="views/home_page.py",
    title="Home",
    icon=":material/home:",
    default=True,
)

add_expense_page = st.Page(
    page="views/add_expense.py",
    title="Add Expense",
    icon=":material/add_circle:",
)

view_expense_page = st.Page(
    page="views/view_expenses.py",
    title="View Expenses",
    icon=":material/visibility:",
)

dashboard_page = st.Page(
    page="views/dashboard.py",
    title="Dashboard",
    icon=":material/bar_chart_4_bars:",
)


about_page = st.Page(
    page="views/about_me.py",
    title="About Me",
    icon=":material/account_circle:",
)


def login():
    st.title("Welcome to TickTrack2 :)")

    st.write("---")

    st.write(
        """
            Welcome to your personalized expense tracker for two! 
            Ready to turn your financial chaos into a well-oiled 
            money machine? Whether you're sharing a budget or just 
            keeping tabs on each other's spending, we've got the tools 
            to help you keep your finances as synced as your favorite 
            playlist. Let's make tracking your pennies together as fun 
            as a double date—minus the awkward small talk!
        """
    )

    st.write("")

    # Check if already logged in
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return  # Exit if already logged in

    # Authentication form
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        with st.form(key="auth_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            submit_button = st.form_submit_button("Login")

            if submit_button:
                # Check credentials from secrets.toml
                if (
                    username == st.secrets["credentials"]["username"]
                    and password == st.secrets["credentials"]["password"]
                ):
                    st.session_state["authenticated"] = True
                    st.session_state["authenticated_user"] = username
                    st.success("Authentication successful! Please set user names.")
                    st.rerun()
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
                        st.rerun()  # Refresh to proceed to the main content
                    else:
                        st.error("Please enter both user names.")


def main():

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    # Display login or main content based on login state
    if st.session_state["logged_in"]:

        pg = st.navigation(
            {
                "Expense Tracker": [
                    home_page,
                    add_expense_page,
                    view_expense_page,
                    dashboard_page,
                ],
                "Contact": [about_page],
            }
        )

        st.sidebar.text("Created by Tanmai Srinath")

        pg.run()

    else:
        login()


if __name__ == "__main__":
    main()
