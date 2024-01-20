from flask import Blueprint, render_template, redirect, session

from modules.logger import logger
from db.models import Users

root = Blueprint("root", __name__, template_folder="templates", static_folder="static")


@root.route("/", methods=["GET"])
def handle_root_request():
    try:
        if "username" in session:
            logger.info(
                f"User {session['username']} already logged in. Attempting to redirect to blog page..."
            )

            user = Users.query.filter_by(username=session["username"]).first()

            logger.info(f"Handling request @ root with user_id: {user.id}")

            return redirect(f"/blog?user={user.id}")
        else:
            logger.info(f"User ID not found, redirecting to bloggers page")

            return redirect("/bloggers")
    except Exception as e:
        logger.exception(f"Error handling request @ root: {e}")

        return render_template("error.html", error=e)
