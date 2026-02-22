from flask import render_template, session
from .config import workout_service, pages_bp

@pages_bp.route("/overview")
def overview() -> str:
    return render_template(
        "pages/overview.html", 
        user_name=session["user_name"]
    )

@pages_bp.route("/create")
def create() -> str:
    workout_types = workout_service.get_workout_types()
    muscle_group = workout_service.get_muscle_groups()
    equipment = workout_service.get_equipment()
    exercises = workout_service.get_exercises()
    return render_template(
        "pages/create.html", 
        user_name=session["user_name"], 
        workout_types=workout_types,
        muscle_group=muscle_group,
        equipment=equipment,
        exercises=exercises
    )

@pages_bp.route("/display")
def display() -> str:
    return render_template(
        "pages/display.html", 
        user_name=session["user_name"]
    )

@pages_bp.route("/statistics")
def statistics() -> str:
    return render_template(
        "pages/statistics.html", 
        user_name=session["user_name"]
    )
