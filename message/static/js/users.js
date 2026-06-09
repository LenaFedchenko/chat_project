import { socket, selectedChatId } from "./openChat.js";


const peopleOnline = document.querySelector(".people-online")
const countUsersP = document.querySelector(".count-users")
const countOnline = document.querySelector(".count-online")

const avatarColors = ["#4DA6FF", "#F39C12", "#1ABC9C", "#9B59B6", "#FF3B30", "#3498DB", "#34495E"]

function avatarColor(userId) {
    return avatarColors[(userId - 1) % avatarColors.length]
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
                    <div class="person">
                        <div class="us" style="background-color: ${avatarColor(user.id)}">${user.first_name.slice(0, 2).toUpperCase()}</div>
                        <p>${user.first_name} ${user.last_name}</p>
                    </div>
                    `
                }else{
                    peopleOnline.innerHTML += `
                    <div class="person">
                        <div class="us" style="background-color: ${avatarColor(user.id)}">${user.first_name.slice(0, 1).toUpperCase()}</div>
                        <p>${user.first_name}</p>
                    </div>
                    `
                }
            }else{
                peopleOnline.innerHTML += `
                <div class="person">
                    <div class="us" style="background-color: ${avatarColor(user.id)}">${user.email.slice(0, 1).toUpperCase()}</div>
                    <p>${user.email}</p>
                </div>
                `
            }
        })

    countUsersP.textContent = `${countUsers} пользователя` 
})


