import smtplib
import ssl
from email.message import EmailMessage
import os
from dotenv import load_dotenv


def send_email_to(email_receiver,subject,content):
    # Load environment variables from .env file
    load_dotenv()

    # Define email sender and receiver
    email_sender = os.environ.get('EMAIL') #'write-email-here'
    email_password = os.environ.get('PWD') #'write-password-here'

    content = f"the message came from :{email_receiver} \nthe content:{content}"

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_sender
    em['Subject'] = subject
    em.set_content(content)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    try:
        # Log in and send the email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_sender, em.as_string())
        return True
    except:
        return False