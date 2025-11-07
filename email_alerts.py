# email_alerts.py
import os
import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  # put in env, not in code

def send_email_alert(receiver_email: str, subject: str, message: str):
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("Email credentials not configured; skipping email send.")
        return False
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email sent to {receiver_email}")
        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
