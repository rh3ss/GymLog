from datetime import datetime
from flask import request, session, redirect, url_for
from ..config import db_create_service, workouts_bp


@workouts_bp.route("/create_workout", methods=["POST"])
def create_workout() -> str:
    if request.method == "POST":
        _create_exercises(workout_id=_create_workout())

    return redirect(url_for("pages.create_page"))


def _create_workout() -> int:
    workout_date_str = request.form.get("workout_date")
    workout_date_obj = datetime.strptime(workout_date_str, "%Y-%m-%d").date()

    return db_create_service.create_workout(
        user_id=session["user_id"],
        workout_type_id=request.form.get("workout_type"),
        workout_name=request.form.get("workout_name"),
        workout_date=workout_date_obj,
        workout_start_time=request.form.get("workout_start_time"),
        workout_end_time=request.form.get("workout_end_time"),
        workout_calories=request.form.get("workout_calories"),
        workout_note=request.form.get("workout_note"),
    )


def _create_exercises(workout_id: int) -> None:
    exercises = request.form.getlist("workout_exercises[]")
    form_data = request.form.to_dict(flat=False)

    for idx, exercise_id in enumerate(exercises):
        exercise_workout_id = db_create_service.create_exercise_workout(
            workout_id=workout_id, exercise_id=exercise_id
        )
        _create_exercise_sets(
            form_data=form_data, idx=idx, exercise_workout_id=exercise_workout_id
        )


def _create_exercise_sets(
    form_data: dict[str, list[str]], idx: int, exercise_workout_id: int
) -> None:
    weights = form_data.get(f"sets[{idx}][weight][]", [])
    reps = form_data.get(f"sets[{idx}][reps][]", [])

    for idx, set_number in enumerate(range(1, len(reps) + 1)):
        db_create_service.create_set(
            exercise_workout_id=exercise_workout_id,
            set_number=set_number,
            weight=weights[idx],
            repetitions=reps[idx],
        )
