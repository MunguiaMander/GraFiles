from flask import Flask, send_from_directory
from config import db

app = Flask(__name__, static_folder="../frontend/static")

@app.route("/")
def index():
    return send_from_directory('../frontend/templates', 'dashboard.html')

@app.route("/static/<path:path>")
def static_dir(path):
    return send_from_directory("../frontend/static", path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
