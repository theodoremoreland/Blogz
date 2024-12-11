from flask import Blueprint, render_template, request

from db.models import Users
from modules.logger import logger

bloggers = Blueprint(
    "bloggers", __name__, template_folder="templates", static_folder="static"
)

PAGE_SIZE = 5


@bloggers.route("/bloggers", methods=["GET"])
def render_bloggers_page():
    logger.info("Rendering bloggers page")

    page = request.args.get(
        "page", 1, type=int
    )  # Get the page number from the query string, default to 1

    try:
        users = Users.query.order_by(Users.username).paginate(
            page=page, per_page=PAGE_SIZE
        )
        post_count_by_user = {}

        for user in users.items:
            post_count = len(user.blog_posts)
            post_count_by_user[user.id] = post_count

        featured_user = users.items[0] if users else None

        return render_template(
            "bloggers.html",
            users_list=users,
            post_count_by_user=post_count_by_user,
            featured_user=featured_user,
        )
    except Exception as e:
        logger.exception(f"Error rendering bloggers page: {e}")

        return render_template("error.html")
