const accountSettings = document.querySelector(".account-settings")
const close2 = document.querySelector(".closing")
const accountSettingsBg = document.querySelector(".account-settings-bg")
const accountSettingsParent = accountSettings.parentElement

document.addEventListener("click", (event) => {
    const us = event.target.closest(".person")
    if (!us) return

    const userId = us.dataset.userId

    openAccountSettings()
    sendDataUser(userId)
})

function openAccountSettings() {
    if (window.matchMedia("(max-width: 480px)").matches) {
        document.body.append(accountSettingsBg, accountSettings)
        accountSettingsBg.style.display = "block"
    }

    accountSettings.style.display = "flex"
}

close2.addEventListener("click", closeAccountSettings)

accountSettingsBg.addEventListener("click", closeAccountSettings)

function closeAccountSettings() {
    accountSettingsBg.style.display = "none"
    accountSettings.style.display = "none"
    accountSettingsParent.append(accountSettings, accountSettingsBg)
}

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
    console.log(data.letters_ava)
    document.querySelector(".letter-avatar").textContent = data.letters_ava || ""

    document.querySelector(".name-last").textContent = data.first_name + " " + data.last_name || ""
    // document.querySelector(".name-last").textContent = data.last_name || ""

    document.querySelector(".username").textContent = "@" + data.username || ""

    document.querySelector(".age").textContent = data.age || ""
    document.querySelector(".gen").textContent = data.gender || ""
}
