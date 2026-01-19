import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
import os

def send_email(recipient: str, subject: str, body: str):
    sender = Config.SMTP_EMAIL
    password = Config.SMTP_PASSWORD
    smtp_server = Config.SMTP_HOST
    smtp_port = Config.SMTP_PORT

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())