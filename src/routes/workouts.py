from flask import Blueprint, render_template, session, redirect, url_for

workouts_bp = Blueprint("workouts", __name__, url_prefix="/workouts")


@workouts_bp.route("/overview")
def overview():
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    return render_template("workouts/overview.html", user_name=session["user_name"])


@workouts_bp.route("/create")
def create():
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    return render_template("workouts/create.html", user_name=session["user_name"])


@workouts_bp.route("/display")
def display():
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    return render_template("workouts/display.html", user_name=session["user_name"])


@workouts_bp.route("/statistics")
def statistics():
    if "user_name" not in session:
        return redirect(url_for("auth.login"))

    return render_template("workouts/statistics.html", user_name=session["user_name"])
