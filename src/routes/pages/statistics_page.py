from flask import render_template, session


def render_statistics_page() -> str:
    return render_template("pages/statistics.html", user_name=session["user_name"])
