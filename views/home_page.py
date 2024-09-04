import streamlit as st

with open("assets/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


st.title("Welcome to Ticktrack2")
st.write("This app allows you to add, view and manage expenses")
