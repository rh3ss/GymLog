from flask import Blueprint, Response, render_template, request, session, redirect, url_for
from utils.dbclient import DBClient
from services.userservice import UserService

auth_bp = Blueprint("auth", __name__)

user_service = UserService(db=DBClient("gymlog.db"))


@auth_bp.route("/")
def index() -> Response:
    return redirect(url_for("auth.login"))

@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        if not (user_service.user_exists(email=request.form["email"]) and 
                user_service.authenticate_user(email=request.form["email"], password=request.form["password"])):
            return render_template("auth/login.html", login_error=True)

        user_data = user_service.get_user(email=request.form["email"])
        session["user_id"] = user_data["user_id"]
        session["user_name"] = user_data["first_name"]
        return redirect(url_for("workouts.overview"))

    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register() -> str:
    if request.method == "POST":
        if user_service.user_exists(request.form["email"]):
            return render_template("auth/register.html", register_error=True)

        user_service.create_user(
            first_name=request.form["first_name"], 
            last_name=request.form["last_name"], 
            email=request.form["email"],
            password=request.form["password"], 
            birthdate=request.form["birthdate"], 
            height_cm=request.form["height_cm"]
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout() -> Response:
    session.clear()
    return redirect(url_for("auth.login"))
