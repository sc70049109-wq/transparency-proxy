from flask import Flask, send_from_directory, redirect, url_for
import subprocess
import os

app = Flask(__name__, static_url_path='/static')

FIREFOX_CONTAINER_NAME = "transparency-firefox"
FIREFOX_IMAGE = "jlesage/firefox:latest"
FIREFOX_PORT = 3001  # fixed port

def start_firefox_container():
    # Check if container is already running
    result = subprocess.run(
        ["docker", "ps", "-q", "-f", f"name={FIREFOX_CONTAINER_NAME}"],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print("Firefox container already running.")
        return

    # Remove any stopped container with the same name
    subprocess.run(["docker", "rm", "-f", FIREFOX_CONTAINER_NAME])

    # Run the Firefox container
    subprocess.run([
        "docker", "run", "-d",
        "--name", FIREFOX_CONTAINER_NAME,
        "-p", f"{FIREFOX_PORT}:5800",  # VNC/GUI port
        FIREFOX_IMAGE
    ])
    print(f"Firefox container started on port {FIREFOX_PORT}.")

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/open-firefox')
def open_firefox():
    start_firefox_container()
    # Redirect to the VNC port for the browser GUI
    return redirect(f"http://localhost:{FIREFOX_PORT}")

if __name__ == '__main__':
    # Make sure the app serves on 0.0.0.0 so other devices can access it
    app.run(host='0.0.0.0', port=8000)
