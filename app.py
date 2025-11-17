#!/usr/bin/env python3
from flask import Flask, jsonify, send_from_directory, request
import subprocess, random, socket

app = Flask(__name__, static_folder='static', static_url_path='')

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/proxy.html')
def proxy():
    return send_from_directory('static', 'proxy.html')

@app.route('/<path:filename>')
def serve_static(filename):
    allowed = ['style.css','script.js']
    if filename in allowed:
        return send_from_directory('static', filename)
    return "Not found", 404

# Helper to pick a free host port
def find_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',0))
    port = s.getsockname()[1]
    s.close()
    return port

# Start a Chromium Docker container
@app.route('/start', methods=['POST'])
def start():
    host_port = find_free_port()
    container_name = f"chromium-{random.randint(1000,9999)}"
    image = "jlesage/chrome:latest"

    try:
        subprocess.run([
            "docker","run","-d",
            "--name", container_name,
            "-p", f"{host_port}:5800",
            image
        ], check=True)
        host = request.host.split(':')[0]
        if host in ("0.0.0.0",""):
            host = "localhost"
        url = f"http://{host}:{host_port}/"
        return jsonify(status="ok", url=url, container_id=container_name)
    except subprocess.CalledProcessError as e:
        return jsonify(status="error", error=str(e)), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
