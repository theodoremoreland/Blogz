from flask import Blueprint, render_template, request, redirect

from modules.logger import logger

root = Blueprint("root", __name__, template_folder="templates", static_folder="static")


@root.route("/")
def handle_root_request():
    try:
        user_id = request.args.get("id")

        logger.info(f"Handling request @ root with user_id: {user_id}")

        if user_id:
            return redirect(f"/blog?user={user_id}")
        else:
            logger.info(f"User ID not found, redirecting to bloggers page")

            return redirect("/bloggers")
    except Exception as e:
        logger.exception(f"Error handling request @ root: {e}")

        return render_template("error.html", error=e)
