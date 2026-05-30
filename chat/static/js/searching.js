const search = document.querySelector(".search")
const searchResults = document.querySelector('.search-results')
const visible = document.querySelector('.visible')

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
                            <h3 class="name">${chat.name_chat}</h3>
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
search.addEventListener('click', () => {
    searchResults.style.display = 'flex'
    visible.style.display = 'none'
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