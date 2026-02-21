from flask import Blueprint, render_template, request, session
from utils.dbclient import DBClient
from services.workoutservice import WorkoutService

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")

workout_service = WorkoutService(db=DBClient("gymlog.db"))

@workouts_bp.route("/overview")
def overview() -> str:
    return render_template("workouts/overview.html", user_name=session["user_name"])

@workouts_bp.route("/create")
def create() -> str:
    workout_types = workout_service.get_workout_types()
    muscle_group = workout_service.get_muscle_groups()
    equipment = workout_service.get_equipment()
    return render_template(
        "workouts/create.html", 
        user_name=session["user_name"], 
        workout_types=workout_types,
        muscle_group=muscle_group,
        equipment=equipment
    )

@workouts_bp.route("/display")
def display() -> str:
    return render_template("workouts/display.html", user_name=session["user_name"])

@workouts_bp.route("/statistics")
def statistics() -> str:
    return render_template("workouts/statistics.html", user_name=session["user_name"])

@workouts_bp.route("/add_workout", methods=["GET", "POST"])
def add_workout() -> str:
    if request.method == "POST":
        workout_service.create_workout(
            user_id=session["user_id"], 
            workout_type_id=request.form.get("workout_type"),
            workout_name=request.form.get("workout_name"),
            workout_date=request.form.get("workout_date"), 
            workout_start_time=request.form.get("workout_start_time"),
            workout_end_time=request.form.get("workout_end_time"), 
            workout_calories=request.form.get("workout_calories"), 
            workout_note=request.form.get("workout_note")
        )

    return render_template("workouts/create.html", user_name=session["user_name"])

@workouts_bp.route("/add_exercise", methods=["GET", "POST"])
def add_exercise() -> str:
    if request.method == "POST":
        workout_service.create_exercise(
            equipment_id=request.form.get("exercise_equipment"),
            muscle_group_id=request.form.get("exercise_muscle_group"),
            name=request.form.get("exercise_name"),
            description=request.form.get("exercise_description")
        )

    return render_template("workouts/create.html", user_name=session["user_name"])