from flask import request, render_template, session, redirect, url_for
from ..config import db_select_service, db_create_service, workouts_bp


@workouts_bp.route("/create_exercise", methods=["POST"])
def create_exercise() -> str:
    if request.method == "POST":
        if db_select_service.do_exercise_already_exists(
            exercise_name=request.form.get("exercise_name")
        ):
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
                exercise_exists_error=True,
            )

        db_create_service.create_exercise(
            equipment_id=request.form.get("exercise_equipment"),
            muscle_group_id=request.form.get("exercise_muscle_group"),
            name=request.form.get("exercise_name"),
            description=request.form.get("exercise_description"),
        )

    return redirect(url_for("pages.create_page"))
