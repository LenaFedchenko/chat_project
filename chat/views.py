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
            my_chats = my_chats
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