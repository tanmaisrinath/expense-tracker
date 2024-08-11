import streamlit as st
from streamlit_lottie import st_lottie
import requests
import time


# Function to load Lottie animation
def load_lottie_url(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Streamlit app


# URL of the Lottie animation JSON file
lottie_url = "https://lottie.host/9ba48063-5bc9-4d51-a990-eded5467941e/WEpBAi2isD.json"

# Load the Lottie animation
lottie_animation = load_lottie_url(lottie_url)

# Create a placeholder for the animation
placeholder = st.empty()

if lottie_animation:
    with placeholder:
        st_lottie(lottie_animation, speed=1, width=600, height=400, key="animation")

    # Duration to display the animation (in seconds)
    duration = 3

    # Wait for the specified duration
    time.sleep(duration)

    # Clear the placeholder after the duration
    placeholder.empty()
else:
    st.error("Failed to load Lottie animation.")
