import flask_socketio, flask_login
from project.settings import socketio
from .model import Message
from project.db import DATABASE
from chat.model import Chat



@socketio.on("connect")
def connection():
    print('Вы подключились')

    socketio.emit(
        "message", 
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
        to= f"room-{chat_id}"
    )

    message =  Message.query.filter_by(chat_id = chat_id).all()
    message_list = []
    for msg in message :
        user_name = msg.user.username
        if user_name is None:
            user_name = "anonimus"
            ava = user_name[:1].upper()
        else:
            ava = user_name[:1].upper()
        message_list.append({
            "username": user_name,
            "time": msg.time_of_msg.strftime("%H:%M"),
            "ava": ava,
            "message": msg.text_of_message
            
        })
    socketio.emit(
        "load_messages", 
        {"messages": message_list},
        to= f"room-{chat_id}"
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
        DATABASE.session.add(message)
        DATABASE.session.commit()
        username = flask_login.current_user.username
        if username == None:
            username = "anonimus"
        socketio.emit(
            "message",
            {
                "message_text": message.text_of_message,
                "chat_id": chat_id,
                "username": username,
                "ava": username[:1].upper(),
                "time": message.time_of_msg.strftime("%H:%M"),
            },
            to= f"room-{chat_id}"
        )

