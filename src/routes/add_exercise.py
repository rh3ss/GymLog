from flask import request, redirect, url_for
from .config import workout_service, workouts_bp

@workouts_bp.route("/add_exercise", methods=["POST"])
def add_exercise() -> str:
    if request.method == "POST":
        workout_service.create_exercise(
            equipment_id=request.form.get("exercise_equipment"),
            muscle_group_id=request.form.get("exercise_muscle_group"),
            name=request.form.get("exercise_name"),
            description=request.form.get("exercise_description")
        )

    return redirect(url_for("pages.create"))