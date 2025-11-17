from flask import Flask, jsonify
import docker
import random

app = Flask(__name__)
client = docker.from_env()

# Change this to a valid Docker image
CHROME_IMAGE = "lscr.io/linuxserver/chrome:latest"

# Port range to assign to new containers
PORT_START = 5900
PORT_END = 5999

def find_free_port():
    """Randomly pick a port for the container"""
    return random.randint(PORT_START, PORT_END)

@app.route("/start", methods=["POST"])
def start_container():
    port = find_free_port()
    container_name = f"transparency_chrome_{port}"

    try:
        container = client.containers.run(
            CHROME_IMAGE,
            name=container_name,
            detach=True,
            ports={"3001/tcp": port},  # 3001 is the exposed GUI port in LS Chrome
            shm_size="2g",             # shared memory for Chromium
        )
    except docker.errors.APIError as e:
        return jsonify({"error": str(e)}), 500

    # Return the URL to open in browser
    url = f"http://localhost:{port}"
    return jsonify({"url": url, "container": container_name})

@app.route("/stop/<container_name>", methods=["POST"])
def stop_container(container_name):
    try:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
        return jsonify({"status": "stopped"})
    except docker.errors.NotFound:
        return jsonify({"error": "container not found"}), 404
    except docker.errors.APIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
