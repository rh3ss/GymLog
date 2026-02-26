from flask import render_template, session
from routes.config import workout_service


def render_create_page() -> str:
    workout_types = workout_service.get_workout_types()
    muscle_group = workout_service.get_muscle_groups()
    equipment = workout_service.get_equipment()
    exercises = workout_service.get_exercises()
    return render_template(
        "pages/create.html",
        user_name=session["user_name"],
        workout_types=workout_types,
        muscle_group=muscle_group,
        equipment=equipment,
        exercises=exercises,
    )
