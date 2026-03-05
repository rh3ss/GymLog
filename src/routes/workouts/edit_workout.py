from datetime import datetime
from flask import request, session, redirect, url_for
from ..config import (
    db_select_service,
    db_create_service,
    db_update_service,
    db_delete_service,
    workouts_bp,
)


@workouts_bp.route("/edit_workout", methods=["POST"])
def edit_workout() -> str:
    if request.method == "POST":
        _edit_current_workout()

    return redirect(url_for("pages.edit_page"))


def _edit_current_workout() -> None:
    _update_workout_attributes()
    submitted_exercises_workouts_ids = request.form.getlist("exercises_workouts_ids[]")
    registered_exercise_ids = request.form.getlist("exercise_ids[]")
    _update_submitted_exercise_workouts(submitted_exercise_workouts=submitted_exercises_workouts_ids)
    _delete_not_submitted_exercise_workouts(
        submitted_exercise_workouts=submitted_exercises_workouts_ids
    )


def _update_workout_attributes() -> None:
    workout_date_str = request.form.get("workout_date")
    workout_date_obj = datetime.strptime(workout_date_str, "%Y-%m-%d").date()

    return db_update_service.update_workout(
        workout_id=request.form.get("workout_id"),
        workout_type_id=request.form.get("workout_type"),
        workout_name=request.form.get("workout_name"),
        workout_date=workout_date_obj,
        workout_start_time=request.form.get("workout_start_time"),
        workout_end_time=request.form.get("workout_end_time"),
        workout_calories=request.form.get("workout_calories"),
        workout_note=request.form.get("workout_note"),
    )


def _update_submitted_exercise_workouts(submitted_exercise_workouts: list[str]) -> None:
    for id in submitted_exercise_workouts:
        exercise_workout_set_ids = request.form.getlist(f"sets_ids[{id}][]")
        exercise_workout_weights = request.form.getlist(f"weights[{id}][]")
        exercise_workout_reps = request.form.getlist(f"reps[{id}][]")

        for i in range(len(exercise_workout_weights)):
            print(
                exercise_workout_set_ids[i],
                exercise_workout_weights[i],
                exercise_workout_reps[i],
            )


def _delete_not_submitted_exercise_workouts(
    submitted_exercise_workouts: list[str],
) -> None:
    workout_id = request.form.get("workout_id")
    exercise_workouts_in_db = db_select_service.get_exercises_workouts_by_workout_ids(
        list_workout_ids=[workout_id]
    )
    db_ids = [str(ew["exercise_workout_id"]) for ew in exercise_workouts_in_db]
    ids_to_delete = [id for id in db_ids if id not in submitted_exercise_workouts]

    for ew_id in ids_to_delete:
        db_delete_service.delete_exercise_workout_entry(exercise_workout_id=ew_id)
