import streamlit as st

# Set up the page configuration with default layout
st.set_page_config(page_title="TickTrack2")

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
</style>
""",
    unsafe_allow_html=True,
)


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

    st.markdown(
        """
    <style>
    .custom-title {
        
        font-size: 55px;
        color: #525252;
        text-align: center;
        margin-top: -20px;
        margin-bottom: -10px;
        font-weight: 600;
    }
    </style>
    <div class="custom-title">Welcome to TickTrack2</div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <style>
    .custom-description {
        
        font-size: 23px;
        color: #525252;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    <div class="custom-description">The Personalized Expense Tracker for Two!</div>
    """,
        unsafe_allow_html=True,
    )

    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        return  # Exit if already logged in

    # Authentication form
    if "authenticated" not in st.session_state or not st.session_state["authenticated"]:
        with st.form(key="auth_form"):

            st.markdown(
                """
                    <style>
                    .custom-description {
                        
                        font-size: 23px;
                        color: #525252;
                        text-align: center;
                                                           
                    }
                    </style>
                    <div class="custom-description">Login</div>
                    """,
                unsafe_allow_html=True,
            )

            username = st.text_input(
                "Username", placeholder="Username", label_visibility="collapsed"
            )
            password = st.text_input(
                "Password",
                placeholder="Password",
                type="password",
                label_visibility="collapsed",
            )

            submit_button = st.form_submit_button("Submit")

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
                user1 = st.text_input(
                    "User 1",
                    key="user1_name",
                    placeholder="User 1",
                    label_visibility="collapsed",
                )
                user2 = st.text_input(
                    "User 2",
                    key="user2_name",
                    placeholder="User 2",
                    label_visibility="collapsed",
                )

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
