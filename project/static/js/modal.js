const buttonSettings = document.querySelector(".open-modal")
const modalSettings = document.querySelector(".modal")
const closeBtn = document.querySelector(".img-set")
const modalBg = document.querySelector(".modal-bg")
const cancel = document.querySelector(".btn-1")

buttonSettings.addEventListener("click", () => {
    modalSettings.style.display = "flex"
    modalBg.style.display = "block"
})

closeBtn.addEventListener("click", () => {
    modalSettings.style.display = "none"
    modalBg.style.display = "none"
})
cancel.addEventListener("click", () => {
    modalSettings.style.display = "none"
    modalBg.style.display = "none"
})

const photoInput = document.getElementById("photoInput");

photoInput.addEventListener("change", async () => {
    const formData = new FormData();
    formData.append("photo", photoInput.files[0]);

    await fetch("/change-photo/", {
        method: "POST",
        body: formData
    });

});
document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});

document.addEventListener('gesturechange', function (e) {
    e.preventDefault();
});

document.addEventListener('gestureend', function (e) {
    e.preventDefault();
});