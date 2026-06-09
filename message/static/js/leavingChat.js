import { socket, selectedChatId } from "./openChat.js"

const leavingButton = document.querySelector('.leaving')
const modalLeave = document.querySelector('.sec2')
const imgClose2 = document.querySelector('.close22')
const btnСancel2 = document.querySelector('.cancel22')
const btnDel = document.querySelector('.delete2')
const messages = document.querySelector('.chat')


socket.on('leave_room', (data) => {
    if (String(data.chat_id) !== String(selectedChatId)) {
        return
    }

    messages.innerHTML += `<p>${data.username} покинув чат</p>`
    socket.emit('get_users', {
        chat_id: selectedChatId
    })
})

leavingButton.addEventListener('click', () => {
    modalLeave.style.display = 'flex'
})

imgClose2.addEventListener('click', () => {
    modalLeave.style.display = 'none'
})


btnСancel2.addEventListener('click', () => {
    modalLeave.style.display = 'none'
})


btnDel.addEventListener('click', () => {
    socket.emit('leave_room', {
        chat_id: selectedChatId
    }, (response) => {
        if (response.status === "success") {
            localStorage.removeItem("selectedChatId")
            location.reload()
        }
    })
    location.reload()
})
