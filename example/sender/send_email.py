"""import smtplib
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
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

def send_email_to(sender_email, sender_password, recipient_email, subject, body):
    # Load environment variables from .env file
    load_dotenv()

    content= f"""
    SENDER : {recipient_email},\n
    SUBJECT :  {subject},\n
    BODY : {body}
    """

    # Create a MIMEText object to represent the email
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = ', '.join([recipient_email,sender_email])
    message['Subject'] = "Message From Portfolio"

    # Attach email body as MIMEText
    if body:
        message.attach(MIMEText(content, 'plain'))

    print(f"Sender Email: {sender_email}")
    print(f"Sender Password: {sender_password}")
    
    try:
        # Connect to the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Start TLS encryption
        server.login(sender_email, sender_password)  # Log in to the server

        # Send the email
        server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")
        return True
    except:
        return False


