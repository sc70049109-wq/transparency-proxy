from flask import Flask, send_from_directory, jsonify
import docker
import os

app = Flask(__name__, static_folder='static')

DOCKER_IMAGE = "jlesage/firefox:latest"
CONTAINER_NAME = "transparency-firefox"
CONTAINER_PORT = 5800
HOST_PORT = 3001

client = docker.from_env()

# Serve index.html at root
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Serve proxy.html if needed
@app.route('/proxy')
def proxy():
    return send_from_directory(app.static_folder, 'proxy.html')

# Open Firefox container
@app.route('/open-firefox')
def open_firefox():
    # Check if container exists
    try:
        container = client.containers.get(CONTAINER_NAME)
        if container.status != 'running':
            container.start()
    except docker.errors.NotFound:
        # Run new container
        container = client.containers.run(
            DOCKER_IMAGE,
            name=CONTAINER_NAME,
            ports={f'{CONTAINER_PORT}/tcp': HOST_PORT},
            shm_size='2g',
            detach=True
        )
    url = f"http://localhost:{HOST_PORT}/"
    return jsonify({'url': url})

# Serve all static files
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
