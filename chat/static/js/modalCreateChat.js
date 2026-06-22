document.addEventListener("DOMContentLoaded", () => {
    const createChat = document.querySelector(".create-chat-class")
    const imgClose = document.querySelector(".close")
    const imgClose2 = document.querySelector(".close2")
    const modal = document.querySelector(".modal-chat")
    const back = document.querySelector(".back")
    const btnCancel = document.querySelector(".cancel")
    const btnCancel2 = document.querySelector(".cancel2")
    const delBtn = document.querySelector(".del")
    const delChat = document.querySelector(".delete")
    const back2 = document.querySelector(".sec")
    const modal2 = document.querySelector(".second")

    const randomColor = `rgb(
        ${Math.floor(Math.random() * 256)},
        ${Math.floor(Math.random() * 256)},
        ${Math.floor(Math.random() * 256)}
    )`;

    if (createChat && modal && back) {
        createChat.addEventListener("click", () => {
            modal.style.display = "flex"
            back.style.display = "flex"
            modal.style.zIndex = "1000"
        })
    }

    if (imgClose && modal && back) {
        imgClose.addEventListener("click", () => {
            modal.style.display = "none"
            back.style.display = "none"
        })
    }

    if (btnCancel && modal && back) {
        btnCancel.addEventListener("click", () => {
            modal.style.display = "none"
            back.style.display = "none"
        })
    }

    if (delBtn) {
        delBtn.addEventListener("click", () => {
            modal2.style.display = "flex"
            back2.style.display = "flex"
            modal2.style.zIndex = "1000"
        })
    }
    if (imgClose2 && modal2 && back2) {
        imgClose2.addEventListener("click", () => {
            modal2.style.display = "none"
            back2.style.display = "none"
        })
    }
    if (btnCancel2 && modal2 && back2) {
        btnCancel2.addEventListener("click", () => {
            modal2.style.display = "none"
            back2.style.display = "none"
        })
    }
    if (delChat) {
        delChat.addEventListener("click", () => {
            deleteChat()
        })
    }
})

async function deleteChat(){
    const response = await fetch("/del-chat/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            del: true
        })
    })
    const data = await response.json()
    if (data.status === "success") {
        window.location.reload()
    }
}
