const search = document.querySelector(".search")
const searchResults = document.querySelector('.search-results')
const visible = document.querySelector('.visible')
const nameChat = document.querySelector(".name-chat")
const rightPart = document.querySelector(".right-part")
const visibleChat = document.querySelector(".chat-place")
const btnBack2 = document.querySelector(".back-chat2")
const mobileMedia = window.matchMedia("(max-width: 480px)")

function isMobileChatLayout() {
    return mobileMedia.matches
}

function resetDesktopLayout() {
    if (!isMobileChatLayout()) {
        rightPart.style.display = ""
        visibleChat.style.display = ""
        btnBack2.style.display = ""
    }
}

mobileMedia.addEventListener("change", resetDesktopLayout)
resetDesktopLayout()

nameChat.addEventListener('click', () =>{
    if (!isMobileChatLayout()) {
        return
    }

    rightPart.style.display = 'flex'
    visibleChat.style.display = 'none'
    btnBack2.style.display = 'flex'
})

btnBack2.addEventListener('click', () => {
    if (!isMobileChatLayout()) {
        return
    }

    visibleChat.style.display = 'flex'
    rightPart.style.display = 'none'
})

search.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        searchingChat(search.value)
    }
})

async function searchingChat(name) {
    const response = await fetch(`/search?name=${name}`)
    const data = await response.json()
    searchResults.innerHTML = ""
    if (data.status === "success") {
        if (data.chats.length === 0) {
            searchResults.innerHTML = `
            <p>Чати не знайдено</p>
            `
            return
        }
        for (const chat of data.chats) {
            searchResults.innerHTML += `
                <div class="example-chat choose" data-id="${chat.id}">
                    <div class="avatar">${chat.img_chat}</div>
                    <div class="all-exam">
                        <div class="name-hact">
                            <p class="name">${chat.name_chat}</p>
                            <p>15m ago</p>
                        </div>
                        <div>
                            <p>${chat.last_msg}</p> 
                        </div>
                    </div>
                </div>
            `
        }
    }
}
search.addEventListener('click', (event) => {
    // stopPropagation зупиняє поширення події на батьківські елементи, щоб уникнути конфліктів з іншими обробниками подій
    event.stopPropagation()
    searchResults.style.display = 'flex'
    visible.style.display = 'none'
})
// Додаємо обробник події на документ, щоб приховати результати пошуку, коли користувач клікає поза межами поля пошуку та результатів
document.addEventListener('click', (event) => {
    if (!search.contains(event.target) && !searchResults.contains(event.target)) {
        searchResults.style.display = 'none'
        visible.style.display = 'flex'
    }
})

searchResults.addEventListener('click', async(event) => {
    const choose = event.target.closest('.choose')
    if (choose){
        await addingChat(choose.dataset.id)
    }
    visible.style.display = 'flex'
})

async function addingChat(chat_id){
    const response = await fetch(`/add-chat?id=${chat_id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: chat_id
        })
    }) 
    const data = await response.json()
    if (data.status === "success") {
        window.location.reload()
    }
}
