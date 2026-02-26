from datetime import datetime, date, timedelta
from flask import request, render_template, session
from .config import workout_service, pages_bp

value_filter_end_date = date.today()
value_filter_start_date = value_filter_end_date - timedelta(days=7)


@pages_bp.route("/overview")
def overview() -> str:
    return render_template("pages/overview.html", user_name=session["user_name"])


@pages_bp.route("/create")
def create() -> str:
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


@pages_bp.route("/display")
def display() -> str:
    workouts = _get_workouts()
    exercises = workout_service.get_exercises()
    workout_ids = [w["workout_id"] for w in workouts]
    exercises_workouts = workout_service.get_exercises_workouts(
        list_workout_ids=workout_ids
    )
    exercise_workout_ids = [ew["exercise_workout_id"] for ew in exercises_workouts]
    sets = workout_service.get_sets(list_exercise_workout_ids=exercise_workout_ids)
    return render_template(
        "pages/display.html",
        user_name=session["user_name"],
        value_filter_start_date=value_filter_start_date,
        value_filter_end_date=value_filter_end_date,
        workouts=workouts,
        exercises=exercises,
        exercises_workouts=exercises_workouts,
        sets=sets,
    )


@pages_bp.route("/statistics")
def statistics() -> str:
    return render_template("pages/statistics.html", user_name=session["user_name"])


def _get_workouts() -> list[tuple]:
    global value_filter_end_date, value_filter_start_date

    filter_start_date = request.args.get("filter_start_date")
    filter_end_date = request.args.get("filter_end_date")
    if not filter_start_date:
        filter_start_date = (date.today() - timedelta(days=7)).isoformat()
    if not filter_end_date:
        filter_end_date = date.today().isoformat()
    value_filter_start_date = filter_start_date
    value_filter_end_date = filter_end_date
    return workout_service.get_workouts(
        user_id=session["user_id"],
        filter_start_day=datetime.strptime(filter_start_date, "%Y-%m-%d").date(),
        filter_end_day=datetime.strptime(filter_end_date, "%Y-%m-%d").date(),
    )
