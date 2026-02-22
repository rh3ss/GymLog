from flask import Flask
import threading
import webbrowser
import time

from routes.config import auth_bp, pages_bp, workouts_bp

def create_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "SECRET_KEY"

    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)
    app.register_blueprint(workouts_bp)

    return app

def open_browser() -> None:
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=False)
