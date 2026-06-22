const selectedChats = document.querySelectorAll(".example-chat")
const messages = document.querySelector(".chat")
const messageForm = document.querySelector(".message-form")
const messageSend = document.querySelector(".typing-field")
const nameChat = document.querySelector('.name-chat')
const noChat = document.querySelector('.no-chat')
const currentUsername = messages.dataset.currentUsername
const currentUserId = messages.dataset.currentUserId
const visibleChat = document.querySelector(".chat-place")
const visibleLeftPart = document.querySelector(".left-part")
const btnBackChat = document.querySelector(".back-chat")
const mobileMedia = window.matchMedia("(max-width: 480px)")
export let selectedChatId = localStorage.getItem("selectedChatId")

export const socket = io()
let previousChatId = null

const avatarColors = ["#4DA6FF", "#F39C12", "#1ABC9C", "#9B59B6", "#FF3B30", "#3498DB", "#34495E"]

function avatarColor(userId) {
    return avatarColors[(userId - 1) % avatarColors.length]}
function getMessageAvatarHTML(msg) {
    if (msg.avatar) {
        const path = msg.avatar.startsWith("/") ? msg.avatar : "/chat/static/" + msg.avatar;
        return `<img src="${path}" alt="" style="width: 100%; height: 100%; object-fit: cover; border-radius: 50%;">`;
    } else {
        return msg.ava;
    }
}
function formatTime(value) {
    const diffMinutes = Math.floor((Date.now() - new Date(value).getTime()) / 60000)
    if (diffMinutes < 1) {
        return "just now"
    }
    if (diffMinutes < 60) {
        return `${diffMinutes}m ago`
    }
    const diffHours = Math.floor(diffMinutes / 60)
    if (diffHours < 24) {
        return `${diffHours}h ago`
    }
    return `${Math.floor(diffHours / 24)}d ago`
}
function formatClockTime(value) {
    if (!value) return ""

    const date = new Date(value)

    const hours = String(date.getHours()).padStart(2, "0")
    const minutes = String(date.getMinutes()).padStart(2, "0")

    return `${hours}:${minutes}`
}
function isMobileChatLayout() {
    return mobileMedia.matches
}

function resetDesktopLayout() {
    if (!isMobileChatLayout()) {
        visibleChat.style.display = ""
        visibleLeftPart.style.display = ""
    }
}

mobileMedia.addEventListener("change", resetDesktopLayout)
resetDesktopLayout()

btnBackChat.addEventListener("click", () => {
    if (!isMobileChatLayout()) {
        return
    }

    visibleChat.style.display = "none"
    visibleLeftPart.style.display = "flex"
})
// сначала скрываем чат и показываем заглушку
messages.style.display = "none"

if (noChat) {
    noChat.style.display = "flex"
}

// если в localStorage был выбранный чат
if (selectedChatId) {
    const activeChat = document.querySelector(`.example-chat[data-id="${selectedChatId}"]`)

    if (activeChat) {
        activeChat.style.backgroundColor = "#F0F8FF"
        messages.style.display = "flex"

        if (noChat) {
            noChat.style.display = "none"
        }
    } else {
        // если такого чата уже нет — чистим localStorage
        selectedChatId = null
        localStorage.removeItem("selectedChatId")
    }
}

if (selectedChatId) {
    const activeChat = document.querySelector(`.example-chat[data-id="${selectedChatId}"]`)

    if (activeChat) {
        activeChat.style.backgroundColor = "#F0F8FF"
        messages.style.display = "flex"
    }
}

socket.on("connect", () => {
    console.log("Ви під'єднались")
    previousChatId = null

    if (selectedChatId) {
        socket.emit("join_room", {
            chat_id: selectedChatId
        })
        socket.emit('get_users', {
            chat_id: selectedChatId
        })

        previousChatId = selectedChatId
    }
})

function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight
}

function myMessageClass(username, userId) {
    if (userId !== undefined && userId !== null) {
        return String(userId) === currentUserId ? "my-message" : ""
    }

    return String(username).trim() === String(currentUsername).trim() ? "my-message" : ""
}

socket.on("join_room", (data) => {
    // console.log(data)
    nameChat.textContent = data.nameChat
})

socket.on("load_messages", (data) => {
    messages.innerHTML = ""
    data.messages.forEach((msg) => {
        const avatarStyle = msg.avatar ? "" : `style="background-color: ${avatarColor(msg.user_id)}"`;

        messages.innerHTML += `
            <div class="msg ${myMessageClass(msg.username, msg.user_id)}">
                <div class="avatar" ${avatarStyle}>
                    ${getMessageAvatarHTML(msg)}
                </div>

                <div class="texts">
                    <div class="sender">
                        <p class="name-sender">${msg.username}</p>
                        <p class="msg-time">${formatClockTime(msg.time)}</p>
                    </div>

                    <p class="msg-sended">${msg.message}</p>
                </div>
            </div>
        `
    });
    scrollToBottom()
})

socket.on("message", (data) => {
    if (String(data.chat_id) !== String(selectedChatId)) {
        return
    }

    const avatarStyle = data.avatar ? "" : `style="background-color: ${avatarColor(data.user_id)}"`;

    messages.innerHTML += `
            <div class="msg ${myMessageClass(data.username, data.user_id)}">
                <div class="avatar" ${avatarStyle}>
                    ${getMessageAvatarHTML(data)}
                </div>

                <div class="texts">
                    <div class="sender">
                        <p class="name-sender">${data.username}</p>
                        <p class="msg-time">${formatClockTime(data.time)}</p>
                    </div>

                    <p class="msg-sended">${data.message_text}</p>
                </div>
            </div>
        `
    scrollToBottom()
    
    const chatItem = document.querySelector(`.example-chat[data-id="${data.chat_id}"]`)
    if (chatItem) {
        const lastMsg = chatItem.querySelector(".last-msg")
        const lastMsgTime = chatItem.querySelector(".name-hact p:last-child")

        if (lastMsg) {
            lastMsg.textContent = data.message_text
        }
        if (lastMsgTime) {
            lastMsgTime.textContent = formatTime(data.time)
        }
    }
})


selectedChats.forEach((chat) => {
    chat.addEventListener("click", () => {
        selectedChats.forEach((item) => {
            item.style.backgroundColor = "transparent"
        })
        if (isMobileChatLayout()) {
            visibleChat.style.display = "flex"
            visibleLeftPart.style.display = "none"
        }
        chat.style.backgroundColor = "#F0F8FF"

        selectedChatId = chat.dataset.id
        localStorage.setItem("selectedChatId", selectedChatId)

        messages.style.display = "flex"

        if (noChat) {
            noChat.style.display = "none"
        }

        if (previousChatId && String(previousChatId) !== String(selectedChatId)) {
            socket.emit("leave_socket_room", {
                chat_id: previousChatId
            })
        }

        socket.emit("join_room", {
            chat_id: selectedChatId
        })
        socket.emit('get_users', {
            chat_id: selectedChatId
        })

        previousChatId = selectedChatId
    })
})
messageForm.addEventListener("submit", (event) => {
    event.preventDefault()
    if (messageSend.value.trim() === "") {
        return
    }
    socket.emit("message", {
        chat_id: selectedChatId,
        message_text: messageSend.value
    })
    messageSend.value = ""
})
