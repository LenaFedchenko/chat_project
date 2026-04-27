import flask
from .settings import main_app
from user.app import user

from user.views import render_register

user.add_url_rule(
    rule = '/register/',
    view_func = render_register,
    methods = ['GET', 'POST']
)


main_app.register_blueprint(
    blueprint = user
)

