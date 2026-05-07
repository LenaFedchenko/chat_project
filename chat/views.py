import flask
import flask_login
# Камилла, сделать проверку что пользователь зареган и 
# потом возвращать в контекст параметре возращать login = True
def render_chat():
    if flask_login.current_user.is_authenticated:
        login = True
        return flask.render_template("chat.html",login=login)
    # в остальных случая перенаправлять на страницу регистрации
    else:
        return flask.redirect("/register")



