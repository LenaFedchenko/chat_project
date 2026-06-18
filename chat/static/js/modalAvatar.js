const avatar = document.querySelector(".opening")
const accountSettings = document.querySelector(".account-settings")
const close2 = document.querySelector(".closing")
const accountSettingsBg = document.querySelector(".account-settings-bg")
const accountSettingsParent = accountSettings.parentElement

avatar.addEventListener("click", () => {
    if (window.matchMedia("(max-width: 480px)").matches) {
        document.body.append(accountSettingsBg, accountSettings)
        accountSettingsBg.style.display = "block"
    }
    accountSettings.style.display = "flex"
})
close2.addEventListener("click", () => {
    accountSettingsBg.style.display = "none"
    accountSettings.style.display = "none"
    accountSettingsParent.append(accountSettings, accountSettingsBg)
})
accountSettingsBg.addEventListener("click", () => {
    close2.click()
})
