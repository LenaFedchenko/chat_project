import smtplib
import email.message as msg
import  dotenv
import os
from dotenv import load_dotenv

load_dotenv()
def send_email(email):
    email_sender = os.getenv("EMAIL_SENDER")
    password_sender = os.getenv("PASSWORD_KEY")
    print(email_sender,password_sender)

    with smtplib.SMTP(host = 'smtp.gmail.com', port = 587) as smtp:
        smtp.starttls()
        smtp.login(user= email_sender, password= password_sender)
        email_msg = msg.EmailMessage()
        
        
        html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Document</title>
            </head>
            <body style="margin: 0; min-height: 100vh; display: flex; align-items: center; justify-content: center; background-color: #F5F5F5; font-family: Arial, sans-serif;">
                <div style="border-radius: 10px; border: 1px #252A5266 solid; background-color:#FFFFFF; width: 68vw; min-height: 66vh; display:flex; align-items: center; justify-content: center; padding: 30px 0;">
                    <div style="width: 30vw; flex-direction: column; gap: 2.4vh; color: black; display:flex;  text-align: left;">
                        <h2 style="font-size: 28px; font-weight: 600; margin: 0;">
                            Вас вітає команда World IT !
                        </h2>
                        <p style="font-size: 16px; line-height: 1.5; margin: 0;">
                            Щоб завершити реєстрацію та переконатися, що саме ви є <br>
                            власником цієї електронної адреси, будь ласка, підтвердіть свою <br>
                            пошту.
                        </p>
                        <button style="width: 30vw; border: none; border-radius: 6px; padding: 10px 22px; background-color: #070A1C; color: white; font-size: 15px; cursor: pointer; text-align: center;">
                            Підтвердити пошту
                        </button>
                        <img src="../static/images/img_friends.png" alt="friends" style="width: 300px; max-width: 100%; align-self: center;">
                        <hr style="width: 30vw; border: none; border-top: 1px #252A5266 solid; margin: 10px 0;">
                        <div style="display: flex; flex-direction: column; justify-content: center;">
                            <p style="font-size: 15px; line-height: 1.5; margin: 0; text-align: left;">
                                Якщо у вас виникнуть питання — ми завжди раді допомогти!<br>
                                З найкращими побажаннями, команда World IT Academy
                            </p>
                        </div>

                    </div>

                </div>

            </body>
            </html>
        """
        email_msg['Subject'] = "theme"
        email_msg['From'] = email_sender
        email_msg['To'] = email


        email_msg.add_alternative(html, subtype = "html")

        smtp.send_message(email_msg)