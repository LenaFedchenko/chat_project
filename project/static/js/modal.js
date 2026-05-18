const buttonSettings = document.querySelector(".open-modal")
const modalSettings = document.querySelector(".modal")
const closeBtn = document.querySelector(".img-set")
const modalBg = document.querySelector(".modal-bg")

buttonSettings.addEventListener("click", () => {
    modalSettings.style.display = "flex"
    modalBg.style.display = "block"
})

closeBtn.addEventListener("click", () => {
    modalSettings.style.display = "none"
    modalBg.style.display = "none"
})