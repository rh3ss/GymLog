from flask import request, redirect, url_for
from ..config import db_update_service, workouts_bp


@workouts_bp.route("/edit_exercise", methods=["POST"])
def edit_exercise() -> str:
    if request.method == "POST":
        db_update_service.update_exercise(
            exercise_id=request.form.get("exercise_id"),
            description=request.form.get("exercise_description"),
        )

    return redirect(url_for("pages.edit_page"))
