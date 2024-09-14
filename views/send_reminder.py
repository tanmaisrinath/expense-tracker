import pywhatkit as w
import time
import pyautogui
import keyboard as k
import datetime
import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

tanmai = st.secrets["tanmai"]
shivangi = st.secrets["shivangi"]


def send_message(message):
    current_time = datetime.datetime.now()
    hour = current_time.hour
    minute = current_time.minute

    phone_number = tanmai["number"]
    wait_time = 15

    call_time = minute + 1
    if call_time <= wait_time:
        call_time = minute + wait_time + 1

    try:
        w.sendwhatmsg(phone_number, message, hour, call_time, wait_time, close_time=2)
    except:
        st.write(
            "Error sending WhatsApp message. Please try again later.\n If you're using a mobile device, this feature is not supported, please use an e-mail reminder instead"
        )

    pyautogui.click(1050, 950)
    time.sleep(2)
    k.press_and_release("enter")


def send_gmail(body):

    sender_email = tanmai["email"]
    receiver_email = shivangi["email"]
    sender_password = tanmai["app_password"]
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Expense Summary - Ticktrack2"
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email sent successfully!")
    except Exception as e:
        st.write(f"An error occured: {e}")
