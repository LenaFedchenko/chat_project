import flask_socketio, flask_login
import flask
from project.settings import socketio
from .model import Message
from project.db import DATABASE
from chat.model import Chat
from user.model import User
from .app import online_users


def _get_chat(chat_id):
    if chat_id is None:
        return None
    try:
        return DATABASE.session.get(Chat, int(chat_id))
    except (TypeError, ValueError):
        return None


def _display_name(user):
    return user.username or user.email


def _avatar_letter(name):
    return name[:1].upper() if name else "?"


def _ensure_creator_in_chat(chat):
    creator = DATABASE.session.get(User, chat.creator_id)
    if creator and creator not in chat.users:
        chat.users.append(creator)
        DATABASE.session.commit()
    return creator


def _chat_users(chat):
    _ensure_creator_in_chat(chat)
    users = []
    seen_ids = set()

    sorted_users = sorted(
        chat.users,
        key=lambda user: (user.id != chat.creator_id, user.id)
    )

    for user in sorted_users:
        if user.id in seen_ids:
            continue
        users.append(user)
        seen_ids.add(user.id)

    return users


def _serialize_user_status(user):
    status = "ON line" if user.id in online_users else "OFF line"
    name = _display_name(user)
    return {
        "id": user.id,
        "username": name,
        "ava": user.avatar or _avatar_letter(name),
        "status": status
    }


def _serialize_chat_user(user):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "avatar": user.avatar
    }


def _serialize_message(msg):
    if msg.user:
        user_name = _display_name(msg.user)
        avatar = msg.user.avatar
    else:
        user_name = "Deleted user"
        avatar = None

    return {
        "username": user_name,
        "user_id": msg.user_id,
        "time": msg.time_of_msg.isoformat(),
        "avatar": avatar,
        "ava": _avatar_letter(user_name),
        "message": msg.text_of_message
    }


@socketio.on("connect")
def connection():
    print('Вы подключились')
    if not flask_login.current_user.is_authenticated:
        return False
    id_user = flask_login.current_user.id
    sid = flask.request.sid
    if id_user not in online_users:
        online_users[id_user] = set()
    online_users[id_user].add(sid)
    
    socketio.emit('user_status_changed', 
        {
            'user_id': id_user,
            'status': 'online'
        }
    )
    
    

@socketio.on("join_room")
def join_room(data):
    chat_id = data.get("chat_id")
    chat = _get_chat(chat_id)
    if not chat:
        return

    flask_socketio.join_room(f"room-{chat_id}")
    socketio.emit(
        "join_room",
        {
            "room": f"room-{chat_id}",
            "nameChat": chat.name_chat
        },
        to= flask.request.sid
    )

    message_list = [
        _serialize_message(msg)
        for msg in Message.query.filter_by(chat_id=chat_id).order_by(Message.time_of_msg.asc()).all()
    ]

    users = _chat_users(chat)
    user_status = [_serialize_user_status(user) for user in users]
    users_online = sum(1 for user in users if user.id in online_users)
    socketio.emit('status_user',
        {
            'status': user_status,
            'chat_id': chat_id,
            'online_users': users_online,
        }, to=f"room-{chat_id}"
    )
    
    socketio.emit(
        "load_messages", 
        {
            "chat_id": chat_id,
            "messages": message_list
        },
        to=flask.request.sid
    )


@socketio.on("message")
def send_message(data):
    chat_id = data.get("chat_id")
    message_text = (data.get("message_text") or "").strip()
    chat = _get_chat(chat_id)
    current_user = flask_login.current_user

    if chat:
        _ensure_creator_in_chat(chat)

    if (
        chat
        and message_text
        and (
            current_user in chat.users
            or chat.creator_id == current_user.id
        )
    ):
        message = Message(
            text_of_message = message_text,
            chat_id = chat_id,
            user_id = current_user.id
        )
        chat.last_msg = message.text_of_message
        DATABASE.session.add(message)
        DATABASE.session.commit()
        
        username = _display_name(current_user)
        
        socketio.emit(
            "message",
            {
                "message_text": message.text_of_message,
                "chat_id": chat_id,
                "username": username,
                "user_id": current_user.id,
                "avatar": current_user.avatar, 
                "ava": _avatar_letter(username),
                "time": message.time_of_msg.isoformat(),
            },
            to=f"room-{chat_id}"
        )


@socketio.on("leave_room")
def leave_room(data):
    chat_id = data.get("chat_id")
    chat = _get_chat(chat_id)

    if not chat:
        return {
            "status": "error",
            "message": "Chat not found",
            "chat_id": chat_id
        }

    current_user = flask_login.current_user
    if not current_user.is_authenticated:
        return {
            "status": "error",
            "message": "Unauthorized",
            "chat_id": chat_id
        }

    username = _display_name(current_user)

    if chat.creator_id == current_user.id:
        deleted_chat_id = chat.id
        socketio.emit("leave_room", {
            "status": "success",
            "chat_id": chat_id,
            "chat_deleted": True,
            "user_leaved": current_user.id,
            "username": username
        }, to=f"room-{chat_id}")

        chat.users.clear()
        DATABASE.session.delete(chat)
        DATABASE.session.commit()
        flask_socketio.leave_room(f"room-{chat_id}")

        return {
            "status": "success",
            "chat_id": deleted_chat_id,
            "chat_deleted": True
        }

    if current_user not in chat.users:
        return {
            "status": "error",
            "message": "User is not in chat",
            "chat_id": chat_id
        }

    message = Message(
        text_of_message = f'{username} покинув чат', 
        chat_id = chat.id, 
        user_id = current_user.id
    )

    DATABASE.session.add(message)
    chat.last_msg = message.text_of_message
    chat.users.remove(current_user)
    DATABASE.session.commit()
    flask_socketio.leave_room(f"room-{chat_id}")

    socketio.emit("leave_room", {
        "status": "success",
        "chat_id": chat_id,
        "chat_deleted": False,
        "user_leaved": current_user.id,
        "username": username
    },
    to=f"room-{chat_id}")

    return {
        "status": "success",
        "chat_id": chat_id,
        "chat_deleted": False
    }


@socketio.on('get_users')
def get_users(data):
    chat_id = data.get("chat_id")
    chat_filter = _get_chat(chat_id)
    if not chat_filter:
        socketio.emit(
            "get_users",
            {
                "status": "404",
                "chat_id": chat_id
            },
            to=flask.request.sid
        )
        return

    users_in_chat = _chat_users(chat_filter)
    users_list = [_serialize_chat_user(user) for user in users_in_chat]
    if users_list:
        socketio.emit("get_users", {
            "status": "success",
            "chat_id": chat_id,
            "users": users_list
        }, to=flask.request.sid)
    else:
        socketio.emit("get_users",
        {
            "status" : "404",
            "chat_id": chat_id
        }, to=flask.request.sid)
        
# выход из комнаты
@socketio.on("leave_socket_room")
def leave_socket_room(data):
    chat_id = data.get("chat_id")
    flask_socketio.leave_room(f"room-{chat_id}")


@socketio.on("disconnect")
def disconnect():
    if not flask_login.current_user.is_authenticated:
        return False
    current_user_id = flask_login.current_user.id
    online_users[current_user_id].discard(flask.request.sid)

    if online_users[current_user_id] == set():
        del online_users[current_user_id]

    socketio.emit("user_status_changed", {
        "user_id" : current_user_id,
        "status": "offline"
    })
