from .settings import main_app
from user.app import user
from chat.app import chat

from user.views import render_register
from user.views import render_login
from chat.views import render_chat

# Камилла создать ссылку на страничку чатов и добавить все импорты

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


main_app.register_blueprint(
    blueprint = user
)

main_app.register_blueprint(
    blueprint= chat
)
