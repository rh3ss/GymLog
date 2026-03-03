from datetime import datetime
from flask import request, session, redirect, url_for
from ..config import workout_service, workouts_bp


@workouts_bp.route("/edit_workout", methods=["POST"])
def edit_workout() -> str:
    if request.method == "POST":
        workout_id = request.form.get("workout_id")
        submitted_exercises = request.form.getlist("exercises_workouts_ids[]")
        exercise_ids = request.form.getlist("exercise_id[]")
        for ew_id in submitted_exercises:
            set_ids = request.form.getlist(f"sets_ids[{ew_id}][]")
            weights = request.form.getlist(f"weights[{ew_id}][]")
            reps = request.form.getlist(f"reps[{ew_id}][]")

            for i in range(len(weights)):
                print(set_ids[i], weights[i], reps[i])

    return redirect(url_for("pages.edit_page"))
