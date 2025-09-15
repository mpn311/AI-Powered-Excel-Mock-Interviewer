import os
from flask import Flask
from flask_session import Session
from dotenv import load_dotenv
from app.routes import bp as core_blueprint

load_dotenv()
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET", "change-this-secret")
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.register_blueprint(core_blueprint)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
