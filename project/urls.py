from .settings import main_app
from user.app import user
from chat.app import chat

from user.views import *
from chat.views import *

chat.add_url_rule(
    rule = '/create-chat/',
    view_func = create_chat_page,
    methods = ['GET', 'POST']
)
chat.add_url_rule(
    rule= "/del-chat/",
    view_func= del_chat,
    methods = ['GET', 'POST']
)

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
user.add_url_rule(
    rule='/get-data/',
    view_func=get_data,
    methods = ['GET', 'POST']
)
user.add_url_rule(
    rule='/del-user/',
    view_func= del_account,
    methods = ['GET', 'POST']
)

main_app.register_blueprint(
    blueprint = user
)

main_app.register_blueprint(
    blueprint= chat
)
