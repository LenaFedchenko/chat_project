from .settings import main_app
from user.app import user
from chat.app import chat
from message.app import message

from user.views import *
from chat.views import *
from message.socket import *


message.add_url_rule(
    rule = '/get-users/',
    view_func = get_users,
    methods = ['GET', 'POST']
)
message.add_url_rule(
    rule = '/leave-socket-room/',
    view_func = leave_socket_room,
    methods = ['GET', 'POST']
)
message.add_url_rule(
    rule= '/leave-room/',
    view_func= leave_room,
    methods= ['GET', 'POST']
)

message.add_url_rule(
    rule = '/connection/',
    view_func = connection,
    methods = ['GET', 'POST']
)
message.add_url_rule(
    rule = '/adding-room/',
    view_func = join_room,
    methods = ['GET', 'POST']
)
message.add_url_rule(
    rule = '/send-message/',
    view_func = send_message,
    methods = ['GET', 'POST']
)
chat.add_url_rule(
    rule = '/send-data-users/',
    view_func = get_data_users,
    methods = ['GET', 'POST']
)
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
    rule="/search/",
    view_func= search,
    methods = ['GET', 'POST']
)
chat.add_url_rule(
    rule="/add-chat/",
    view_func= add_chat,
    methods = ['GET', 'POST']
)

chat.add_url_rule(
    rule= "/",
    view_func= render_chat,
    methods = ['GET', 'POST']
)
user.add_url_rule(
    rule= '/success/',
    view_func= success,
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
main_app.register_blueprint(
    blueprint= message
)
