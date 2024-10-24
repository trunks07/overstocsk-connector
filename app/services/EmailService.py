import smtplib
from email.mime.text import MIMEText
from app.settings.environment import Env

class EmailService:
    # Function to send an email
    async def send_error_email(subject: str, body: str, recipient: str):
        # Set up SMTP server credentials
        smtp_server = Env.EMAIL_SERVER
        smtp_port = Env.EMAIL_PORT
        sender_email = Env.EMAIL_ADDRESS
        sender_password = Env.EMAIL_PASSWORD

        # Create the email content
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient, msg.as_string())