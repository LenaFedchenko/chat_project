import smtplib
import email.message as msg
import email.mime.image as mime_image
import os
import flask
from dotenv import load_dotenv

load_dotenv()
def send_email(email, user_id):
    email_sender = os.getenv("EMAIL_SENDER")
    password_sender = os.getenv("PASSWORD_KEY")
    print(email_sender,password_sender)

    with smtplib.SMTP(host = 'smtp.gmail.com', port = 587) as smtp:
        smtp.starttls()
        smtp.login(user= email_sender, password= password_sender)
        email_msg = msg.EmailMessage()
        # http://1200:700:8000:/check_email?user_id=5
        link = flask.url_for("user.check_email", user_id= user_id, _external = True)
        html = f"""
            <!DOCTYPE html>
            <html lang="uk">
            <head>
                <meta charset="UTF-8">
                <title>Підтвердження пошти</title>
            </head>

            <body style="margin: 0; padding: 0; background-color: #F5F5F5; font-family: Arial, sans-serif;">

                <div style="padding: 2.5rem 0.9375rem; background-color: #F5F5F5;">

                    <div style="max-width: 38.75rem; margin: 0 auto; padding: 2.5rem; background-color: #FFFFFF; border: 0.0625rem solid #252A5266; border-radius: 0.625rem; box-sizing: border-box; color: #070A1C;">

                        <h2 style="font-size: 1.75rem; font-weight: 600; margin: 0 0 1.25rem 0;">
                            Вас вітає команда World IT!
                        </h2>

                        <p style="font-size: 1rem; line-height: 1.5; margin: 0 0 1.5rem 0;">
                            Щоб завершити реєстрацію та переконатися, що саме ви є
                            власником цієї електронної адреси, будь ласка, підтвердіть свою пошту.
                        </p>

                        <a href="{link}" style="display: block; width: 100%; padding: 0.75rem 1.25rem; box-sizing: border-box; background-color: #070A1C; color: #FFFFFF; text-align: center; text-decoration: none; border-radius: 0.375rem; font-size: 0.9375rem; margin-bottom: 1.5rem;">
                            Підтвердити пошту
                        </a>

                        <div style="text-align: center; margin-bottom: 1.5rem;">
                            <img src="cid:image1" alt="friends" style="display: block; width: 18.75rem; max-width: 100%; margin: 0 auto;">
                        </div>

                        <hr style="border: none; border-top: 0.0625rem solid #252A5266; margin: 1.25rem 0;">

                        <p style="font-size: 0.9375rem; line-height: 1.5; margin: 0;">
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