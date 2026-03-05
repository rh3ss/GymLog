from datetime import datetime, date, timedelta
from flask import request, render_template, session
from routes.config import db_select_service

value_filter_end_date = date.today()
value_filter_start_date = value_filter_end_date - timedelta(days=7)


def render_edit_page() -> str:
    workouts = _get_all_workouts_by_date_filtering()
    exercises = db_select_service.get_exercises_with_equipment_and_musclegroup()
    workout_ids = [w["workout_id"] for w in workouts]
    exercises_workouts = db_select_service.get_exercises_workouts_by_workout_ids(
        list_workout_ids=workout_ids
    )
    exercise_workout_ids = [ew["exercise_workout_id"] for ew in exercises_workouts]
    sets = db_select_service.get_sets_by_exercise_workout_ids(
        list_exercise_workout_ids=exercise_workout_ids
    )

    return render_template(
        "pages/edit.html",
        user_name=session["user_name"],
        value_filter_start_date=value_filter_start_date,
        value_filter_end_date=value_filter_end_date,
        workouts=workouts,
        exercises=exercises,
        exercises_workouts=exercises_workouts,
        sets=sets,
    )


def _get_all_workouts_by_date_filtering() -> list[tuple]:
    global value_filter_end_date, value_filter_start_date

    filter_start_date = request.args.get("filter_start_date")
    filter_end_date = request.args.get("filter_end_date")
    if not filter_start_date:
        filter_start_date = (date.today() - timedelta(days=7)).isoformat()
    if not filter_end_date:
        filter_end_date = date.today().isoformat()
    value_filter_start_date = filter_start_date
    value_filter_end_date = filter_end_date

    return db_select_service.get_workouts_by_date_filtering(
        user_id=session["user_id"],
        filter_start_day=datetime.strptime(filter_start_date, "%Y-%m-%d").date(),
        filter_end_day=datetime.strptime(filter_end_date, "%Y-%m-%d").date(),
    )
