
const accountSettings = document.querySelector(".account-settings")
const close2 = document.querySelector(".closing")
const accountSettingsBg = document.querySelector(".account-settings-bg")
const accountSettingsParent = accountSettings.parentElement
const mobileChatQuery = "(max-width: 768px), (max-height: 480px) and (hover: none) and (pointer: coarse)"

document.addEventListener("click", (event) => {
    const us = event.target.closest(".person")
    if (!us) return

    const userId = us.dataset.userId

    openAccountSettings()
    sendDataUser(userId)
})

function openAccountSettings() {
    if (window.matchMedia(mobileChatQuery).matches) {
        document.body.append(accountSettingsBg, accountSettings)
        accountSettingsBg.style.display = "block"
    }

    accountSettings.style.display = "flex"
}

function closeAccountSettings() {
    accountSettingsBg.style.display = "none"
    accountSettings.style.display = "none"
    accountSettingsParent.append(accountSettings, accountSettingsBg)
}

close2.addEventListener("click", closeAccountSettings)
accountSettingsBg.addEventListener("click", closeAccountSettings)

async function sendDataUser(id_user) {
    try {
        const response = await fetch("/send-data-users/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ id_us: id_user })
        })

        const data = await response.json()
        renderUser(data)

    } catch (error) {
        console.error("Ошибка загрузки пользователя:", error)
    }
}

function renderUser(data) {
    const avatarImg = accountSettings.querySelector(".avatar-img")
    const avatarText = accountSettings.querySelector(".letter-avatar")

    if (data.avatar) {
        let path = data.avatar

        if (!path.startsWith("/")) {
            path = "/chat/static/" + path
        }

        avatarImg.src = path
        avatarImg.style.display = "block"
        avatarText.style.display = "none"
    } else {
        avatarImg.style.display = "none"
        avatarText.style.display = "block"
        avatarText.textContent = data.letters_ava || ""
    }

    accountSettings.querySelector(".name-last").textContent =
        ((data.first_name || "") + " " + (data.last_name || "")).trim()

    accountSettings.querySelector(".username").textContent =
        "@" + (data.username || "")

    accountSettings.querySelector(".age").textContent = data.age || ""
    accountSettings.querySelector(".gen").textContent = data.gender || ""
}
const btnDeleteAvatar = document.querySelector(".btn-del")

btnDeleteAvatar.addEventListener("click", async () => {
    try {
        const response = await fetch("/delete-avatar/", {
            method: "POST"
        })

        const data = await response.json()

        if (data.status === "success") {
            location.reload()
        }
    } catch (error) {
        console.error(error)
    }
})
