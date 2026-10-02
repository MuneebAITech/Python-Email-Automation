import smtplib
from email.message import EmailMessage


class EmailSender:

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send_email(self,receiver_email,subject,html_content,attachment_path=None):

        msg = EmailMessage()

        msg["Subject"] = subject
        msg["From"] = self.email
        msg["To"] = receiver_email

        msg.add_alternative(
            html_content,
            subtype="html"
        )
        
        if attachment_path:

            with open(
                attachment_path,
                "rb"
            ) as file:

                file_data = file.read()

                file_name = attachment_path.split("/")[-1]

            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="octet-stream",
                filename=file_name
            )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                self.email,
                self.password
            )

            smtp.send_message(msg)