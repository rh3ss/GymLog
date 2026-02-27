from routes.config import pages_bp
from routes.pages.overview_page import render_overview_page
from routes.pages.create_page import render_create_page
from routes.pages.edit_page import render_edit_page
from routes.pages.statistics_page import render_statistics_page


@pages_bp.route("/overview")
def overview_page() -> str:
    return render_overview_page()


@pages_bp.route("/create")
def create_page() -> str:
    return render_create_page()


@pages_bp.route("/edit")
def edit_page() -> str:
    return render_edit_page()


@pages_bp.route("/statistics")
def statistics_page() -> str:
    return render_statistics_page()
