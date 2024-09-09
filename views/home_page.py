import streamlit as st
from streamlit_lottie import st_lottie
import requests

# Function to load Lottie animation from a URL
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

# Load Lottie animation from URL
lottie_animation = load_lottie_url("https://lottie.host/de99ae94-af7f-4e52-a6a2-12f309a9ab27/PFgjWk5QN2.json")

# Display the Lottie animation on the page
st_lottie(lottie_animation, key="example_animation", height=300, width=300)

# Example content on the page
st.title("Welcome to TickTrack2!")
st.write("Join forces and keep your expenses in check—because managing money is more fun when you’ve got a partner in budget crime!")
