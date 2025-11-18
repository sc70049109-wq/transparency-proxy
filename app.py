from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="static")

@app.route("/")
def root():
    # Serve /static/index.html as the homepage
    return send_from_directory("static", "index.html")

@app.route("/<path:path>")
def static_proxy(path):
    # Serve any file inside /static
    return send_from_directory("static", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
