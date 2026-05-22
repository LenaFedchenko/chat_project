from .settings import main_app
from user.app import user
from chat.app import chat

from user.views import render_register
from user.views import render_login
from chat.views import render_chat, get_data
from user.views import check_email


chat.add_url_rule(
    rule= "/",
    view_func= render_chat,
    methods = ['GET', 'POST']
)

user.add_url_rule(
    rule = '/login/',
    view_func = render_login,
    methods = ['GET', 'POST']
)

user.add_url_rule(
    rule = '/register/',
    view_func = render_register,
    methods = ['GET', 'POST']
)

user.add_url_rule(
    rule = '/check_email/',
    view_func = check_email,
    methods = ['GET', 'POST']
)
# Саша, создать юрл для функции get_data 
user.add_url_rule(
    rule='/get-data/',
    view_func=get_data,
    methods = ['GET', 'POST']

)

main_app.register_blueprint(
    blueprint = user
)

main_app.register_blueprint(
    blueprint= chat
)
