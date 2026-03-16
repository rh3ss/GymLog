from flask import request, render_template, session, redirect, url_for
from ..config import db_select_service, db_update_service, workouts_bp


@workouts_bp.route("/edit_exercise", methods=["POST"])
def edit_exercise() -> str:
    if request.method == "POST":
        db_update_service.update_exercise(
            exercise_id=request.form.get("exercise_id"),
            description=request.form.get("exercise_description"),
        )

    return redirect(url_for("pages.edit_page"))
