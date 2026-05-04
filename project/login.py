from user.model import User
import flask_login
import secrets
from .settings import main_app

# Генерирует 32-байтный (64 символа) случайный hex-ключ
token = secrets.token_hex(32)
manager = flask_login.LoginManager(main_app)
main_app.secret_key = token



@manager.user_loader
def get_user(user_id):
    return User.query.get(user_id)
