import streamlit as st

# Load secrets
secrets = st.secrets["credentials"]


def login_screen():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        if username == secrets["username"] and password == secrets["password"]:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid username or password")


def main_screen():
    st.title("TickTrack2")


def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        main_screen()
    else:
        login_screen()


if __name__ == "__main__":
    main()
