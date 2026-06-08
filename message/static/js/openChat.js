const selectedChats = document.querySelectorAll(".example-chat")
const messages = document.querySelector(".chat")
const messageForm = document.querySelector(".message-form")
const messageSend = document.querySelector(".typing-field")
const nameChat = document.querySelector('.name-chat')
const noChat = document.querySelector('.no-chat')
const currentUsername = messages.dataset.currentUsername
const currentUserId = messages.dataset.currentUserId

export let selectedChatId = localStorage.getItem("selectedChatId")

export const socket = io()

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
    // console.log("Ви під'єднались")

    if (selectedChatId) {
        socket.emit("join_room", {
            chat_id: selectedChatId
        })
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
    // console.log("loded messages", data.messages)
    messages.innerHTML = ""
    data.messages.forEach((msg) => {
        messages.innerHTML += `
            <div class="msg ${myMessageClass(msg.username, msg.user_id)}">
                <div class="avatar">${msg.ava}</div>

                <div class="texts">
                    <div class="sender">
                        <p class="name-sender">${msg.username}</p>
                        <p class="time">${msg.time}</p>
                    </div>
                    <p class="msg-sended">${msg.message}</p>
                </div>
            </div>
        `
    });
    scrollToBottom()
})

socket.on("message", (data) => {
    messages.innerHTML += `
            <div class="msg ${myMessageClass(data.username, data.user_id)}">
                <div class="avatar">${data.ava}</div>

                <div class="texts">
                    <div class="sender">
                        <p class="name-sender">${data.username}</p>
                        <p class="time">${data.time}</p>
                    </div>

                    <p class="msg-sended">${data.message_text}</p>
                </div>
            </div>
        `
    scrollToBottom()
    location.reload()
})


selectedChats.forEach((chat) => {
    chat.addEventListener("click", () => {
        selectedChats.forEach((item) => {
            item.style.backgroundColor = "transparent"
        })

        chat.style.backgroundColor = "#F0F8FF"

        selectedChatId = chat.dataset.id
        localStorage.setItem("selectedChatId", selectedChatId)

        messages.style.display = "flex"

        if (noChat) {
            noChat.style.display = "none"
        }

        socket.emit("join_room", {
            chat_id: selectedChatId
        })
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
