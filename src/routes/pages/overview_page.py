from flask import render_template, session


def render_overview_page() -> str:
    return render_template("pages/overview.html", user_name=session["user_name"])
