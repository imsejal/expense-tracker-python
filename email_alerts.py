# email_alerts.py
"""
Simple email-sending utility for alerts.

Credentials must be provided via environment variables:
- SENDER_EMAIL
- SENDER_PASSWORD

This module handles failures Prints message and returns False.
"""

import os
import smtplib
from email.mime.text import MIMEText


SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")  #app password not gmail password


def send_email_alert(receiver_email: str, subject: str, message: str) -> bool:
    """
    Try to send an email using Gmail's SMTP server. Returns True on success.
    If credentials are not configured or sending fails, logs the error and returns False.
    """
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
        print(f"Email sent to {receiver_email}")
        return True
    except Exception as e:
        # Handles email failure
        print(f"Email sending failed: {e}")
        return False
