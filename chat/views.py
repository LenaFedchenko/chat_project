import flask
from flask import jsonify, request
import flask_login
from datetime import datetime
from user.model import User
from project.db import DATABASE
from .model import Chat
from message.model import Message


def last_message_time(chat):
    last_message = Message.query.filter_by(chat_id=chat.id).order_by(Message.time_of_msg.desc()).first()
    if not last_message:
        return ""
    minutes = int((datetime.now() - last_message.time_of_msg).total_seconds() // 60)
    if minutes < 1:
        return "just now"
    if minutes < 60:
        return f"{minutes}m ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours}h ago"
    days = hours // 24
    return f"{days}d ago"

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
        for chat in all_chats:
            chat.last_msg_time = last_message_time(chat)
        if created_chat:
            created_chat.last_msg_time = last_message_time(created_chat)
        user_filter= User.query.filter_by(
            id = user.id
        ).scalar()
        if user_filter.first_name is not None and user_filter.last_name is not None:
            letters_ava =  user_filter.first_name[0] + user_filter.last_name[0]
        else: 
            letters_ava = user_filter.email[:2]
        try: 
            my_chats = user.chats
        except: 
            my_chats = None
        return flask.render_template(
            "chat.html",
            login=True,
            created_chat=created_chat,
            all_chats=all_chats,
            chats_list=[],
            modal= False,
            my_chats = my_chats,
            user = user,
            letters_ava= letters_ava
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
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if username:
                user.username = username
            if gender: 
                user.gender = gender
            if birth_date:
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
                    img_chat = chat_name[:2].upper(),
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
        search = data.get('del')
        if search:
            user = flask_login.current_user
            chat_delete = Chat.query.filter_by(creator_id = user.id).first()
            chat_delete.users.clear()
            DATABASE.session.delete(chat_delete)
            DATABASE.session.commit()
            
        return {
            "status": "success",
            "search": search
        }


def search():
    name_of_chat = flask.request.args.get("name")
    print(name_of_chat)
    if name_of_chat:
        finded_chats = Chat.query.filter(Chat.name_chat.ilike(f"%{name_of_chat}%")).all()
        finded_chat_list = []
        for chat in finded_chats:
            finded_chat_list.append({
                "id": chat.id,
                "name_chat": chat.name_chat,
                "img_chat": chat.img_chat,
                "last_msg": chat.last_msg
                , "last_msg_time": last_message_time(chat)
            })
        return {
            "status": "success",
            "chats": finded_chat_list
        }
    
def add_chat():
    data = flask.request.get_json()
    id = data.get('id')
    user = flask_login.current_user
    chat = Chat.query.get(int(id))

    if user not in chat.users:
        chat.users.append(user)
        DATABASE.session.commit()
    return {
            "status": "success"
        }

def get_data_users():
    data = flask.request.get_json()
    user_id = data.get("id_us")

    filtered_user = User.query.filter_by(id=user_id).first()

    if not filtered_user:
        return jsonify({"error": "user not found"}), 404

    if filtered_user.first_name and filtered_user.last_name:
        letters_ava = filtered_user.first_name[0] + filtered_user.last_name[0]
        first_name = filtered_user.first_name
        last_name = filtered_user.last_name
    else:
        letters_ava = filtered_user.email[:2]
        first_name = "Немає ім'я"
        last_name = "Немає прізвище"

    username = filtered_user.username or "Немає нікнейму"
    age = filtered_user.age or "Немає дати народження"
    gender = filtered_user.gender or "Немає статі"

    return jsonify({
        "letters_ava": letters_ava,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "age": age,
        "gender": gender
    })
