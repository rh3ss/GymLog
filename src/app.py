from flask import Flask
import threading
import webbrowser
import time
import socket

from routes.config import auth_bp, pages_bp, workouts_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "SECRET_KEY"

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(workouts_bp)

    return app

def wait_for_server(host="127.0.0.1", port=5000):
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            time.sleep(0.2)

def open_browser():
    wait_for_server()
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    app = create_app()
    threading.Thread(target=open_browser).start()
    app.run(host="127.0.0.1", port=5000, debug=False)
