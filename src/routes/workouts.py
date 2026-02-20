from flask import Blueprint, render_template, request, session, redirect, url_for
from utils.dbclient import DBClient
from services.workoutservice import WorkoutService

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")

workout_service = WorkoutService(db=DBClient("gymlog.db"))

@workouts_bp.route("/overview")
def overview() -> str:
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    return render_template("workouts/overview.html", user_name=session["user_name"])

@workouts_bp.route("/create")
def create() -> str:
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    workout_types = workout_service.get_workout_type()
    return render_template("workouts/create.html", user_name=session["user_name"], workout_types=workout_types)

@workouts_bp.route("/display")
def display() -> str:
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    return render_template("workouts/display.html", user_name=session["user_name"])

@workouts_bp.route("/statistics")
def statistics() -> str:
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    return render_template("workouts/statistics.html", user_name=session["user_name"])

@workouts_bp.route("/add", methods=["GET", "POST"])
def add_workout():
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        workout_service.create_workout(
            user_id=session["user_id"], workout_type_id=request.form.get("workout_type"), workout_date=request.form.get("workout_date"), workout_start_time=request.form.get("workout_start_time"),
            workout_end_time=request.form.get("workout_end_time"), workout_calories=request.form.get("workout_calories"), workout_note=request.form.get("workout_note")
        )
        return create()

    return render_template("workouts/create.html", user_name=session["user_name"])

