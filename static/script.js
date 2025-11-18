document.getElementById("enter-proxy-btn").addEventListener("click", async (e) => {
    e.preventDefault(); // prevent default link behavior
    try {
        const res = await fetch("/open-firefox");
        if (res.redirected) {
            window.location.href = res.url; // redirect to Firefox container
        }
    } catch (err) {
        console.error("Error opening Firefox container:", err);
        alert("Failed to start Firefox container. Check console for details.");
    }
});
