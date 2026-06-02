const selectedChats = document.querySelectorAll(".example-chat")
const messages = document.querySelector(".chat")
const messageForm = document.querySelector(".message-form")
const messageSend = document.querySelector(".typing-field")

let selectedChatId = null


const socket = io()


socket.on("join_room", (data) => {
    console.log(data)
})

socket.on("load_messages", (data) => {
    console.log("loded messages", data.messages)
    messages.innerHTML = ""
    data.messages.forEach((msg) => {
        messages.innerHTML += `
            <div class="msg">
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
})

socket.on("message", (data) => {
    messages.innerHTML += `
            <div class="msg">
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

})


selectedChats.forEach((chat) => {
    chat.addEventListener("click", () => {
        messages.style.display = "flex"
        selectedChatId = chat.dataset.id
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