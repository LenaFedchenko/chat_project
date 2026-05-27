import flask
import flask_login
from user.model import User
from project.db import DATABASE
from .model import Chat

def render_chat():
    if flask_login.current_user.is_authenticated:
        login = True
        user = flask_login.current_user
        created_chat = Chat.query.filter_by(
            creator_id=user.id
        ).first()
        all_chats = Chat.query.filter(
            Chat.users.any(User.id == user.id)
        ).all()
        return flask.render_template(
            "chat.html",
            login=True,
            created_chat=created_chat,
            all_chats=all_chats,
            chats_list=[],
            modal= False
        )
    else:
        return flask.redirect("/register")



def get_data():
    if flask.request.method == "POST":
        first_name = flask.request.form.get("first_name")
        last_name = flask.request.form.get("last_name")
        username = flask.request.form.get("username")
        gender = flask.request.form.get("gender")
        birth_date = flask.request.form.get("birth_date")
        user = User.query.filter_by(id = flask_login.current_user.id).scalar()
        if user is not None:
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.gender = gender
            user.age = birth_date

            DATABASE.session.commit()
            return flask.redirect("/")


def create_chat_page():
    if flask.request.method == "POST":
        chat_name = flask.request.form["chat_name"]

        user = flask_login.current_user
        is_create = Chat.query.filter_by(
                creator_id=user.id
            ).first()

        if is_create is None:
            if chat_name:
                new_chat = Chat(
                    name_chat = chat_name,
                    img_chat = "avatar.png",
                    last_msg = "Чат пустий",
                    creator_id=user.id,
                    users = [user]
                    )
                
                DATABASE.session.add(new_chat)
                DATABASE.session.commit()
                return flask.redirect("/")
        else:
            return flask.redirect("/")
    return flask.make_response({"status":"success"})


def del_chat():
    if flask.request.method == "POST":
        data = flask.request.get_json()

        search = data.get("del")

        if search:
            user = flask_login.current_user
            is_create = Chat.query.filter_by(
                creator_id=user.id
            ).first()
            is_create.users.clear()
            DATABASE.session.delete(is_create)
            DATABASE.session.commit()

        return {
            "status": "success",
            "search": search
        }
    
