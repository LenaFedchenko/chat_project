import smtplib
import email.message as msg
import  dotenv
import os
from dotenv import load_dotenv

load_dotenv()
def send_email():
    email_sender = os.getenv("EMAIL_SENDER")
    password_sender = os.getenv("PASSWORD_KEY")
    print(email_sender,password_sender)

    with smtplib.SMTP(host = 'smtp.gmail.com', port = 587) as smtp:
        smtp.starttls()
        smtp.login(email_sender, password_sender )
        email_msg = msg.EmailMessage()
        
        
        html = "<p>Натискаючи «Продовжити», ви погоджуєтеся з нашими</p>"
        email_msg['Subject'] = "theme"
        email_msg['From'] = email_sender
        email_msg['To'] = "kulikkarolina17@gmail.com"


        email_msg.add_alternative(html, subtype = "html")

        smtp.send_message(email_msg)