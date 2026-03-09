from flask import request, redirect, url_for
from ..config import db_select_service, db_delete_service, workouts_bp

@workouts_bp.route("/delete_workout", methods=["POST"])
def delete_workout() -> str:
    if request.method == "POST":
        _delete_workout_references()

    return redirect(url_for("pages.edit_page"))


def _delete_workout_references() -> None:
    workout_id = request.form.get("workout_id")
    workout_id = 16
    _delete_exercise_workouts_references(workout_id=workout_id)
    db_delete_service.delete_workout_entry(workout_id=workout_id)


def _delete_exercise_workouts_references(workout_id: int) -> None:
    exercises_workouts_in_db = db_select_service.get_exercises_workouts_by_workout_ids(list_workout_ids=[workout_id])
    exercises_workouts_ids = [
        str(ew["exercise_workout_id"]) for ew in exercises_workouts_in_db
    ]

    _delete_sets_references(exercises_workouts_ids=exercises_workouts_ids)

    for ew_id in exercises_workouts_ids:
        db_delete_service.delete_exercise_workout_entry(exercise_workout_id=ew_id)


def _delete_sets_references(exercises_workouts_ids: list[str]) -> None:
    sets_in_db = db_select_service.get_sets_by_exercise_workout_ids(list_exercise_workout_ids=exercises_workouts_ids)
    sets_ids = [str(id["set_entry_id"]) for id in sets_in_db]

    for set_id in sets_ids:
        db_delete_service.delete_set_entry(set_entry_id=set_id)
