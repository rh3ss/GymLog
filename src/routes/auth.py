from flask import Blueprint, render_template, request, redirect, url_for, session
from utils.dbclient import DBClient
from services.userservice import UserService

auth_bp = Blueprint("auth", __name__)

db = DBClient("gymlog.db")
user_service = UserService(db=db)


@auth_bp.route("/")
def index():
    return redirect(url_for("auth.login"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if not (user_service.user_exists(email=email) and user_service.authenticate_user(email, password)):
            return render_template("auth/login.html", login_error=True)

        session["user_name"] = user_service.get_user_name(email)
        return redirect(url_for("workouts.overview"))

    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if user_service.user_exists(request.form["email"]):
            return render_template("auth/register.html", register_error=True)

        user_service.create_user(
            first_name=request.form["first_name"], last_name=request.form["last_name"], email=request.form["email"],
            password=request.form["password"], birthdate=request.form["birthdate"], height_cm=request.form["height_cm"]
        )
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
