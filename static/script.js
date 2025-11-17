// Dark / light mode toggle
const themeBtn = document.getElementById("theme-toggle");
themeBtn?.addEventListener("click", () => {
    if(document.body.style.filter === "brightness(1.2)") {
        document.body.style.filter = "brightness(1)";
    } else {
        document.body.style.filter = "brightness(1.2)";
    }
});
