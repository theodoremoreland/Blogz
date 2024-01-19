from flask import Blueprint, render_template

from db.models import Users
from modules.logger import logger

bloggers = Blueprint(
    "bloggers", __name__, template_folder="templates", static_folder="static"
)


@bloggers.route("/bloggers")
def render_bloggers_page():
    try:
        users = Users.query.all()

        return render_template("bloggers.html", users_list=users)
    except Exception as e:
        logger.exception(f"Error rendering home page: {e}")

        return render_template("error.html", error=e)
