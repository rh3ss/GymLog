from flask import render_template, session
from routes.config import db_select_service


def render_overview_page() -> str:
    last_workout = db_select_service.get_last_completed_workout(
        user_id=session["user_id"]
    )
    last_exercises_workout = db_select_service.get_exercises_workouts_by_workout_ids(
        list_workout_ids=[last_workout[0]["workout_id"]]
    )
    last_exercises_workout_ids = [
        ew["exercise_workout_id"] for ew in last_exercises_workout
    ]
    last_exercises_sets = db_select_service.get_sets_by_exercise_workout_ids(
        list_exercise_workout_ids=last_exercises_workout_ids
    )

    return render_template(
        "pages/overview.html",
        user_name=session["user_name"],
        last_workout=last_workout,
        last_exercises_workout=last_exercises_workout,
        last_exercises_sets=last_exercises_sets,
    )
