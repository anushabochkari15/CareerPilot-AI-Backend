from email.message import EmailMessage
import smtplib
import ssl

from app.config import settings


class EmailService:

    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.sender_email = settings.SENDER_EMAIL
        self.sender_password = settings.SENDER_PASSWORD

        print("SMTP Server:", self.smtp_server)
        print("SMTP Port:", self.smtp_port)
        print("Sender Email:", self.sender_email)
        print("Password Length:", len(self.sender_password))

    def send_email(self, receiver_email, subject, body):

        message = EmailMessage()

        message["From"] = self.sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.set_content(body)

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)

            return True

        except Exception as e:
            print(f"Email sending failed: {e}")
            return False

    def send_registration_email(self, email, username):

        subject = "Welcome to CareerPilot 🎉"

        body = f"""
Hello {username},

Welcome to CareerPilot!

Your account has been successfully created.

We're excited to help you in your career journey.

Happy Learning!

Regards,
CareerPilot Team
"""

        return self.send_email(email, subject, body)

    def send_login_email(self, email, username):

        subject = "Welcome Back to CareerPilot 👋"

        body = f"""
Hello {username},

You have successfully logged into CareerPilot.

If this wasn't you, please reset your password immediately.

Regards,
CareerPilot Team
"""

        return self.send_email(email, subject, body)