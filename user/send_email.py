import smtplib
import email.message as msg
import email.mime.image as mime_image
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
            <html lang="uk">
            <head>
                <meta charset="UTF-8">
                <title>Підтвердження пошти</title>
            </head>

            <body style="margin: 0; padding: 0; background-color: #F5F5F5; font-family: Arial, sans-serif;">

                <div style="padding: 40px 15px; background-color: #F5F5F5;">

                    <div style="max-width: 620px; margin: 0 auto; padding: 40px; background-color: #FFFFFF; border: 1px solid #252A5266; border-radius: 10px; box-sizing: border-box; color: #070A1C;">

                        <h2 style="font-size: 28px; font-weight: 600; margin: 0 0 20px 0;">
                            Вас вітає команда World IT!
                        </h2>

                        <p style="font-size: 16px; line-height: 1.5; margin: 0 0 24px 0;">
                            Щоб завершити реєстрацію та переконатися, що саме ви є
                            власником цієї електронної адреси, будь ласка, підтвердіть свою пошту.
                        </p>

                        <a href="https://example.com" style="display: block; width: 100%; padding: 12px 20px; box-sizing: border-box; background-color: #070A1C; color: #FFFFFF; text-align: center; text-decoration: none; border-radius: 6px; font-size: 15px; margin-bottom: 24px;">
                            Підтвердити пошту
                        </a>

                        <div style="text-align: center; margin-bottom: 24px;">
                            <img src="cid:image1" alt="friends" width="300" style="display: block; max-width: 100%; margin: 0 auto;">
                        </div>

                        <hr style="border: none; border-top: 1px solid #252A5266; margin: 20px 0;">

                        <p style="font-size: 15px; line-height: 1.5; margin: 0;">
                            Якщо у вас виникнуть питання — ми завжди раді допомогти!<br>
                            З найкращими побажаннями, команда World IT Academy
                        </p>

                    </div>

                </div>

            </body>
            </html>
        """
        email_msg['Subject'] = "Підтвердження паролю"
        email_msg['From'] = email_sender
        email_msg['To'] = email


        email_msg.add_alternative(html, subtype = "html")
        path = os.path.abspath(os.path.join(__file__, "..", "static", "images", "img_friends.png"))
        with open(path, mode = "rb") as file:
            data = file.read()
            
            image = mime_image.MIMEImage(data)
            image.add_header("Content-ID", "<image1>")
            email_msg.attach(image)

        smtp.send_message(email_msg)