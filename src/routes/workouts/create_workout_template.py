from datetime import datetime
from flask import request, session, redirect, url_for
from ..config import db_create_service, workouts_bp


@workouts_bp.route("/create_workout_template", methods=["POST"])
def create_workout_template() -> str:
    if request.method == "POST":
        _create_workout_template_exercises(
            workout_template_id=_create_workout_template()
        )

    return redirect(url_for("pages.create_page"))


def _create_workout_template() -> int:
    return db_create_service.create_workout_template(
        user_id=session["user_id"],
        workout_name=request.form.get("workout_name"),
    )


def _create_workout_template_exercises(workout_template_id: int) -> None:
    exercises = request.form.getlist("workout_exercises[]")

    for idx, exercise_id in enumerate(range(1, len(exercises) + 1)):
        db_create_service.create_exercise_workout_template(
            workout_template_id=workout_template_id,
            exercise_id=exercise_id,
            order_number=idx,
        )
