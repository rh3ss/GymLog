from flask import render_template, session
from routes.config import db_select_service


def render_create_page() -> str:
    workout_types = db_select_service.get_workout_types()
    muscle_group = db_select_service.get_muscle_groups()
    equipment = db_select_service.get_equipment()
    exercises = db_select_service.get_exercises_with_equipment_and_musclegroup()

    return render_template(
        "pages/create.html",
        user_name=session["user_name"],
        workout_types=workout_types,
        muscle_group=muscle_group,
        equipment=equipment,
        exercises=exercises,
    )
