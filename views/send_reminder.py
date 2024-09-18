import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

tanmai = st.secrets["tanmai"]
shivangi = st.secrets["shivangi"]


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
