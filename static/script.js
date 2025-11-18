document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("enter-proxy-btn");

  btn.addEventListener("click", async (e) => {
    e.preventDefault();

    // Open about:blank first
    const newTab = window.open("about:blank", "_blank");

    try {
      const response = await fetch("/open-firefox");
      if (!response.ok) throw new Error("Failed to start Firefox container");

      const data = await response.json();
      if (data.url) {
        // Navigate the new tab to the container URL
        newTab.location.href = data.url;
      } else {
        newTab.close();
        alert("Failed to get Firefox URL from backend.");
      }
    } catch (err) {
      newTab.close();
      alert(`Error opening Firefox container: ${err.message}`);
      console.error(err);
    }
  });
});
