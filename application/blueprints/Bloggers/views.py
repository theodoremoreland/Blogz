from flask import Blueprint, render_template

from db.models import Users
from modules.logger import logger

bloggers = Blueprint(
    "bloggers", __name__, template_folder="templates", static_folder="static"
)


@bloggers.route("/bloggers", methods=["GET"])
def render_bloggers_page():
    logger.info("Rendering bloggers page")

    try:
        users = Users.query.order_by(Users.username).all()
        post_count_by_user = {}

        for user in users:
            post_count = len(user.blog_posts)
            post_count_by_user[user.id] = post_count

        featured_user = users[6] if users else None

        return render_template(
            "bloggers.html",
            users_list=users,
            post_count_by_user=post_count_by_user,
            featured_user=featured_user,
        )
    except Exception as e:
        logger.exception(f"Error rendering bloggers page: {e}")

        return render_template("error.html")
