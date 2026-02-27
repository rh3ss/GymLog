from flask import render_template, session
from routes.config import workout_service


def render_overview_page() -> str:
    last_workout = workout_service.get_last_workout(user_id=session["user_id"])
    last_exercises_workout = workout_service.get_exercises_workouts(
        list_workout_ids=[last_workout[0]["workout_id"]]
    )
    last_exercises_workout_ids = [
        ew["exercise_workout_id"] for ew in last_exercises_workout
    ]
    last_exercises_sets = workout_service.get_sets(
        list_exercise_workout_ids=last_exercises_workout_ids
    )
    return render_template(
        "pages/overview.html",
        user_name=session["user_name"],
        last_workout=last_workout,
        last_exercises_workout=last_exercises_workout,
        last_exercises_sets=last_exercises_sets,
    )
