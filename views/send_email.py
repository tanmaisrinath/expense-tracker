import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, to_email, from_email, password):
    # Create message object
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach the body of the email
    msg.attach(MIMEText(body, "plain"))

    try:
        # Set up the SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)  # For Gmail
        server.starttls()  # Upgrade the connection to secure

        # Log in to the server
        server.login(from_email, password)

        # Send the email
        server.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        # Close the server connection
        server.quit()


# Usage example
send_email(
    subject="Hello",
    body="Reply to me pls",
    to_email="shivangishashi99@gmail.com",
    from_email="tanmaisrinath1@gmail.com",
    password="qtzj bcbq koja poot",
)


# TO DO:
# 1. Reminder email on the 5th of every month showing the amount owed, monthly total.
# 2.
