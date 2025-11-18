document.addEventListener('DOMContentLoaded', () => {
    const enterBtn = document.getElementById('enter-proxy');

    enterBtn.addEventListener('click', async () => {
        // Open blank tab first
        const newTab = window.open('about:blank', '_blank');

        try {
            const res = await fetch('/open-firefox');
            const data = await res.json();

            // Inject iframe pointing to container
            const iframe = newTab.document.createElement('iframe');
            iframe.src = data.url;
            iframe.style.width = '100vw';
            iframe.style.height = '100vh';
            iframe.style.border = 'none';
            newTab.document.body.style.margin = '0';
            newTab.document.body.appendChild(iframe);
        } catch (err) {
            newTab.document.body.innerHTML = `<h2 style="color:red;">Failed to start Firefox container. Check console for details.</h2>`;
            console.error(err);
        }
    });
});
