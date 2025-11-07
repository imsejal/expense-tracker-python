import smtplib
from email.mime.text import MIMEText

# Configure your email credentials (use a dummy Gmail or your own)
SENDER_EMAIL = "sejal.cse@gmail.com"
SENDER_PASSWORD = "Shrisa@5644"

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
