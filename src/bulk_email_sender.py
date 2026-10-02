import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from email_sender import EmailSender
from logger import log_success, log_failed
from email_validator import validate_email, EmailNotValidError
from report_generator import create_report


def send_bulk_emails(excel_file,progress_callback=None):
    print("FUNCTION STARTED")
        
    # Load .env file
    load_dotenv()


    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


    # Load HTML template
    env = Environment(
        loader=FileSystemLoader("templates")
    )

    template = env.get_template(
        "email_template.html"
    )


    # Create Email Sender Object
    sender = EmailSender(
        EMAIL_ADDRESS,
        EMAIL_PASSWORD
    )

    pdf_files = list(
        Path("attachments").glob("*.pdf")
    )

    attachment_path = None

    if pdf_files:

        attachment_path = str(
            pdf_files[0]
        )

    print(attachment_path)

    data = pd.read_excel(
        excel_file
    )

    data.columns = data.columns.str.strip() # for maintain the wrong input excel file
    total_rows = len(data)
    total_emails = 0
    sent_emails = 0
    failed_emails = 0

    # Send Emails
    for index, row in data.iterrows():
        total_emails += 1

        receiver_email = row["email"]
        name = row["name"]
        subject = row["subject"]
        attachment_path = row["attachment"]
        print(attachment_path)


        try:
            validate_email(receiver_email)

        except EmailNotValidError:

            print(
                f"❌ Invalid Email: {receiver_email}"
            )

            log_failed(
                receiver_email,
                "Invalid Email Format"
            )

            failed_emails += 1

            continue


        html_content = template.render(
            name=name
        )

        try:

            sender.send_email(
                receiver_email,
                subject,
                html_content,
                attachment_path
            )

            
            print(
                f"✅ Email Sent To: {name}"
            )

            sent_emails += 1

            log_success(
                name,
                receiver_email
            )

        except Exception as e:
            failed_emails += 1

            print(
                f"❌ Failed: {receiver_email}"
            )

            print(e)

            log_failed(
                receiver_email,
                str(e)
            )

            if progress_callback:

                progress_callback(
                    (index + 1) / total_rows
                )


    print("\n" + "=" * 33)

    print(
        f"Total Emails : {total_emails}"
    )

    print(
        f"Sent         : {sent_emails}"
    )

    print(
        f"Failed       : {failed_emails}"
    )

    

    print("=" * 33)

    create_report(
        total_emails,
        sent_emails,
        failed_emails
    )