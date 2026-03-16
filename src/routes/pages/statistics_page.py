from flask import render_template, session
from routes.config import db_select_service


def render_statistics_page() -> str:
    user_id = session["user_id"]

    total_calories = db_select_service.get_total_calories_burnd(user_id=user_id)
    avg_calories = db_select_service.get_avg_calories(user_id=user_id)
    total_duration = db_select_service.get_total_duration(user_id=user_id)
    avg_duration = db_select_service.get_avg_workout_duration(user_id=user_id)

    workout_type_distribution = db_select_service.get_workout_type_distribution(
        user_id=user_id
    )
    top_exercises = db_select_service.get_top_exercises(user_id=user_id)

    workout_labels = [row[0] for row in workout_type_distribution]
    workout_data = [row[1] for row in workout_type_distribution]

    exercise_labels = [row[0] for row in top_exercises]
    exercise_data = [row[1] for row in top_exercises]

    return render_template(
        "pages/statistics.html",
        total_calories=total_calories,
        avg_calories=avg_calories,
        total_duration=total_duration,
        avg_duration=avg_duration,
        workout_labels=workout_labels,
        workout_data=workout_data,
        exercise_labels=exercise_labels,
        exercise_data=exercise_data,
    )
