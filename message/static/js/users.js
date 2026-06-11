import { socket, selectedChatId } from "./openChat.js";


const peopleOnline = document.querySelector(".people-online")
const countUsersP = document.querySelector(".count-users")
const countOnline = document.querySelector(".count-online")

const avatarColors = ["#4DA6FF", "#F39C12", "#1ABC9C", "#9B59B6", "#FF3B30", "#3498DB", "#34495E"]

function avatarColor(userId) {
    return avatarColors[(userId - 1) % avatarColors.length]
}

function updateOnlineUsers(){
    const onlineUsers = document.querySelectorAll('.status-circle[data-status="online"]')
    countOnline.textContent = `${onlineUsers.length} online`
}

    
socket.on('get_users', (data) => {
    if (String(data.chat_id) !== String(selectedChatId)) {
        return
    }

    const users = Array.isArray(data.users) ? data.users : []
    let countUsers = 0
    peopleOnline.innerHTML = ""

    users.forEach((user) => {
        countUsers ++
        if (user.first_name) {
            if (user.last_name) {
                peopleOnline.innerHTML += `
                    <div class="person" data-user-id="${user.id}">
                        <div class="us" style="background-color: ${avatarColor(user.id)}">
                            ${user.first_name.slice(0, 1).toUpperCase()}
                            <span class="status-circle"></span>
                        </div>
                        <div>
                            <p>${user.first_name} ${user.last_name}</p>
                        </div>
                    </div>
                    `
                }else{
                    peopleOnline.innerHTML += `
                    <div class="person" data-user-id="${user.id}">
                        <div class="us" style="background-color: ${avatarColor(user.id)}">
                            ${user.first_name.slice(0, 1).toUpperCase()}
                            <span class="status-circle"></span>
                        </div>
                        <div>
                            <p>${user.first_name}</p>
                        </div>
                    </div>
                    `
                }
            }else{
                peopleOnline.innerHTML += `
                <div class="person" data-user-id="${user.id}">
                    <div class="us" style="background-color: ${avatarColor(user.id)}">
                        ${user.email.slice(0, 1).toUpperCase()}
                        <span class="status-circle"></span>
                    </div>
                    <div>
                        <p>${user.email}</p>
                    </div>
                </div>
                `
            }
        })

    countUsersP.textContent = `${countUsers} пользователя` 
})

socket.on('status_user', (data) => {
    if(String(data.chat_id) !== String(selectedChatId)){
        return
    }
    console.log(data.online_users)
    data.status.forEach((userStatus) => {
        const person = document.querySelector(`.person[data-user-id="${userStatus.id}"]`)
        if (!person){ return }
        const status = person.querySelector(".status-circle")
        

        if(status){
            if(userStatus.status.includes("ON line") || userStatus.status === "online"){
                status.style.backgroundColor = "#007AFF"
                status.dataset.status = "online"
            }else{
                status.style.backgroundColor = "#999999"
                status.dataset.status = "offline"
            }
        }
    })

    countOnline.textContent = `${data.online_users} online`
})


socket.on('disconnect', () => {
    console.log("Вы отсоеденились")
}) 


socket.on("user_status_changed", (data) => {
    const person = document.querySelector(`.person[data-user-id="${data.user_id}"]`)
    if (!person){ return }
    const status = person.querySelector(".status-circle")

    if (status) {
        if (data.status === 'online') {
            status.style.backgroundColor = "#007AFF"
            status.dataset.status = "online"
        }else{
            status.style.backgroundColor = "#999999"
            status.dataset.status = "offline"
        }
        updateOnlineUsers()
    }

    
    
})

