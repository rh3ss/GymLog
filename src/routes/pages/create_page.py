from flask import jsonify, render_template, session
from routes.config import workouts_bp, db_select_service


def render_create_page() -> str:
    workout_types = db_select_service.get_workout_types()
    workout_templates = db_select_service.get_workout_templates(
        user_id=session["user_id"]
    )
    muscle_group = db_select_service.get_muscle_groups()
    equipment = db_select_service.get_equipment()
    exercises = db_select_service.get_exercises_with_equipment_and_musclegroup()

    return render_template(
        "pages/create.html",
        user_name=session["user_name"],
        workout_types=workout_types,
        workout_templates=workout_templates,
        muscle_group=muscle_group,
        equipment=equipment,
        exercises=exercises,
    )


@workouts_bp.route("/get_workout_template_exercises/<int:template_id>")
def get_workout_template_exercises(template_id: int):
    rows = db_select_service.get_workout_template_exercises_by_template_id(
        workout_template_id=template_id
    )

    return jsonify([dict(row) for row in rows])
