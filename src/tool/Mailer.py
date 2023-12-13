import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:

    def __init__(self):
        self.sender_email = os.environ.get("MAIL_SENDER")
        self.receiver_email = os.environ.get("MAIL_RECIPIENT")
        self.email_password = os.environ.get("SMTP_PASSWORD")
        self.smtp_server = os.environ.get("SMTP_SERVER")
        self.smtp_port = os.environ.get("SMTP_PORT")
    
    def send_notification_email(self, subject, message):
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver_email
        msg["Subject"] = subject
        body = message
        msg.attach(MIMEText(body, "plain"))
        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.sender_email, self.email_password)
        text = msg.as_string()
        server.sendmail(self.sender_email, self.receiver_email, text)
        server.quit()