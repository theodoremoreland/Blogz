from flask import Blueprint, render_template, Flask, request, redirect

from db.models import Users, BlogPosts
from modules.logger import logger

home = Blueprint("home", __name__, template_folder="templates", static_folder="static")


@home.route("/")
def render_home_page():
    try:
        user_id = request.args.get("id")

        logger.info(f"Rendering home page with user_id: {user_id}")

        if user_id:
            return redirect(f"/blog?user={user_id}")
        else:
            users = Users.query.all()

            return render_template("home.html", users_list=users)
    except Exception as e:
        logger.exception(f"Error rendering home page: {e}")

        return render_template("error.html", error=e)
