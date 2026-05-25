const createChat = document.querySelector(".create-chat-class")
const imgClose = document.querySelector(".close")
const modal = document.querySelector(".modal-chat")
const back = document.querySelector(".back")
const btnCancel = document.querySelector(".cancel")


createChat.addEventListener("click", () => {
    modal.style.display = "flex"
    back.style.display = "flex"
    modal.style.zIndex = "1000"
})


imgClose.addEventListener("click", () => {
    modal.style.display = "none"
    back.style.display = "none"
})
btnCancel.addEventListener("click", () => {
    modal.style.display = "none"
    back.style.display = "none"
})
