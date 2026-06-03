const selectedChats = document.querySelectorAll(".example-chat")
const messages = document.querySelector(".chat")
const messageForm = document.querySelector(".message-form")
const messageSend = document.querySelector(".typing-field")
const nameChat = document.querySelector('.name-chat')
const currentUsername = messages.dataset.currentUsername

let selectedChatId = localStorage.getItem("selectedChatId")

const socket = io()

if (selectedChatId) {
    const activeChat = document.querySelector(`.example-chat[data-id="${selectedChatId}"]`)

    if (activeChat) {
        activeChat.style.backgroundColor = "#F0F8FF"
        messages.style.display = "flex"
    }
}

socket.on("connect", () => {
    console.log("Ви під'єднались")

    if (selectedChatId) {
        socket.emit("join_room", {
            chat_id: selectedChatId
        })
    }
})

function scrollToBottom() {
    messages.scrollTop = messages.scrollHeight
}

function myMessageClass(username) {
    return username === currentUsername ? "my-message" : ""
}
// выделение одного чата
selectedChats.forEach((chat) => {
    chat.addEventListener("click", () => {
        selectedChats.forEach((item) => {
            item.style.backgroundColor = "transparent"
        })
        chat.style.backgroundColor = "#F0F8FF"
    })
})

socket.on("join_room", (data) => {
    console.log(data)
    nameChat.textContent = data.nameChat
})

socket.on("load_messages", (data) => {
    console.log("loded messages", data.messages)
    messages.innerHTML = ""
    data.messages.forEach((msg) => {
        messages.innerHTML += `
            <div class="msg ${myMessageClass(msg.username)}">
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
            <div class="msg ${myMessageClass(data.username)}">
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

})


selectedChats.forEach((chat) => {
    chat.addEventListener("click", () => {
        selectedChats.forEach((item) => {
            item.style.backgroundColor = "transparent"
        })

        chat.style.backgroundColor = "#F0F8FF"
        messages.style.display = "flex"

        selectedChatId = chat.dataset.id
        localStorage.setItem("selectedChatId", selectedChatId)

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
