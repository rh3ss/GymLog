from flask import request, session, redirect, url_for
from .config import workout_service, workouts_bp

@workouts_bp.route("/add_workout", methods=["POST"])
def add_workout() -> str:
    if request.method == "POST":
        exercise_ids = request.form.getlist("workout_exercises[]")
        workout_id = _create_workout_get_id()

    return redirect(url_for("pages.create"))

def _create_workout_get_id() -> int:
    return workout_service.create_workout(
        user_id=session["user_id"], 
        workout_type_id=request.form.get("workout_type"),
        workout_name=request.form.get("workout_name"),
        workout_date=request.form.get("workout_date"), 
        workout_start_time=request.form.get("workout_start_time"),
        workout_end_time=request.form.get("workout_end_time"), 
        workout_calories=request.form.get("workout_calories"), 
        workout_note=request.form.get("workout_note")
    )
