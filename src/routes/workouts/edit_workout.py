from datetime import datetime
from flask import request, redirect, url_for
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
    _update_submitted_exercise_workouts()
    _delete_not_submitted_exercise_workouts()
    _create_new_registered_exercises_workouts()


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


def _update_submitted_exercise_workouts() -> None:
    submitted_exercises_workouts_ids = request.form.getlist("exercises_workouts_ids[]")
    registered_exercise_ids = request.form.getlist("exercise_ids[]")
    workout_id = request.form.get("workout_id")

    for idx, ew_id in enumerate(submitted_exercises_workouts_ids):
        db_update_service.update_exercise_workout(
            exercise_workout_id=ew_id,
            workout_id=workout_id,
            exercise_id=registered_exercise_ids[idx],
        )


def _create_new_registered_exercises_workouts() -> None:
    submitted_exercises_workouts_ids = request.form.getlist("exercises_workouts_ids[]")
    registered_exercise_ids = request.form.getlist("exercise_ids[]")
    workout_id = request.form.get("workout_id")
    start_idx = len(submitted_exercises_workouts_ids)

    for idx_positive, idx_negativ in zip(
        range(start_idx, len(registered_exercise_ids)),
        range(-1, -(len(registered_exercise_ids) - start_idx + 1), -1),
    ):
        new_exercise_workout_id = db_create_service.create_exercise_workout(
            workout_id=workout_id, exercise_id=registered_exercise_ids[idx_positive]
        )
        _create_new_registered_exercises_workouts_sets(
            array_idx=idx_negativ, exercise_workout_id=new_exercise_workout_id
        )


def _create_new_registered_exercises_workouts_sets(
    array_idx: int, exercise_workout_id: int
) -> None:
    weights = request.form.getlist(f"weights[{array_idx}][]")
    reps = request.form.getlist(f"reps[{array_idx}][]")

    for idx, set_number in enumerate(range(1, len(reps) + 1)):
        db_create_service.create_set(
            exercise_workout_id=exercise_workout_id,
            set_number=set_number,
            weight=weights[idx],
            repetitions=reps[idx],
        )


def _delete_not_submitted_exercise_workouts() -> None:
    submitted_exercises_workouts_ids = request.form.getlist("exercises_workouts_ids[]")
    workout_id = request.form.get("workout_id")
    exercise_workouts_in_db = db_select_service.get_exercises_workouts_by_workout_ids(
        list_workout_ids=[workout_id]
    )
    exercise_workouts_db_ids = [
        str(ew["exercise_workout_id"]) for ew in exercise_workouts_in_db
    ]
    exercise_workouts_ids_to_delete = [
        id
        for id in exercise_workouts_db_ids
        if id not in submitted_exercises_workouts_ids
    ]

    for ew_id in exercise_workouts_ids_to_delete:
        db_delete_service.delete_exercise_workout_entry(exercise_workout_id=ew_id)
