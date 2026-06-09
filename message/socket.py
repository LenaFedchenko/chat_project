import flask_socketio, flask_login
from project.settings import socketio
from .model import Message
from project.db import DATABASE
from chat.model import Chat
import flask



@socketio.on("connect")
def connection():
    print('Вы подключились')

    socketio.emit(
        "connection_status",
        {
            "status": "success"
        }
    )

@socketio.on("join_room")
def join_room(data):
    chat_id = data.get("chat_id")
    name_chat = Chat.query.filter_by(id= chat_id).scalar()
    flask_socketio.join_room(f"room-{chat_id}")
    socketio.emit(
        "join_room",
        {
            "room": f"room-{chat_id}",
            "nameChat": name_chat.name_chat
        },
        to= flask.request.sid
    )

    message =  Message.query.filter_by(chat_id = chat_id).all()
    message_list = []
    for msg in message :
        user_name = msg.user.username
        if user_name is None:
            user_name = msg.user.email
            ava = user_name[:1].upper()
        else:
            ava = user_name[:1].upper()
        message_list.append({
            "username": user_name,
            "user_id": msg.user_id,
            "time": msg.time_of_msg.strftime("%H:%M"),
            "ava": ava,
            "message": msg.text_of_message
            
        })
    socketio.emit(
        "load_messages", 
        {"messages": message_list},
        to= flask.request.sid
    )


@socketio.on("message")
def send_message(data):
    chat_id = data.get("chat_id")
    message_text =  data.get("message_text")
    if chat_id and message_text:
        message = Message(
            text_of_message = message_text,
            chat_id = chat_id,
            user_id = flask_login.current_user.id
        )
        chat_filter_id = Chat.query.filter_by(id= chat_id).scalar()
        chat_filter_id.last_msg = message.text_of_message
        DATABASE.session.add(message)
        DATABASE.session.commit()
        username = flask_login.current_user.username
        if username == None:
            username = flask_login.current_user.email
        socketio.emit(
            "message",
            {
                "message_text": message.text_of_message,
                "chat_id": chat_id,
                "username": username,
                "user_id": flask_login.current_user.id,
                "ava": username[:1].upper(),
                "time": message.time_of_msg.strftime("%H:%M"),
            },
            to= f"room-{chat_id}"
        )


@socketio.on("leave_room")
def leave_room(data):
    chat_id = data.get("chat_id")

    chat_filter_id2 = Chat.query.filter_by(id= chat_id).scalar()

    current_user = flask_login.current_user
    if current_user.username is not None:
        username = current_user.username
    else:
        username = current_user.email
        
    message = Message(
        text_of_message = f'{username} покинув чат', 
        chat_id = chat_filter_id2.id, 
        user_id = current_user.id
    )

    DATABASE.session.add(message)
    if chat_filter_id2.creator_id == current_user.id:
        chat_filter_id2.users.clear()
        DATABASE.session.delete(chat_filter_id2)
    elif current_user in chat_filter_id2.users:
        chat_filter_id2.users.remove(current_user)
    DATABASE.session.commit()
    flask_socketio.leave_room(f"room-{chat_id}")

    socketio.emit("leave_room", {
        "status": "success",
        "chat_id": chat_id,
        "user_leaved": current_user.id,
        "username": username
    },
    to=f"room-{chat_id}")


@socketio.on('get_users')
def get_users(data):
    chat_id = data.get("chat_id")
    chat_filter = Chat.query.filter_by(id = chat_id).first()
    users_in_chat = chat_filter.users
    users_list = []
    if users_in_chat:
        for user in users_in_chat:
            users_list.append({
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username" : user.username
                })
        socketio.emit("get_users", {
            "status": "success",
            "chat_id": chat_id,
            "users": users_list
        }, to=f"room-{chat_id}")
    else:
        socketio.emit("get_users",
        {
            "status" : "404",
            "chat_id": chat_id
        }, to=f"room-{chat_id}")
        
# выход из комнаты
@socketio.on("leave_socket_room")
def leave_socket_room(data):
    chat_id = data.get("chat_id")
    flask_socketio.leave_room(f"room-{chat_id}")
