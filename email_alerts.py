import smtplib
from email.mime.text import MIMEText

SENDER_EMAIL = "sample@gmail.com"
SENDER_PASSWORD = "Sample@123"

def send_email_alert(receiver_email, subject, message):
    try:
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        print(f"📧 Email sent to {receiver_email}")
    except Exception as e:
        print(f"Email sending failed: {e}")
