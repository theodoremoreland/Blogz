from flask import Blueprint, render_template

from db.models import Users, BlogPosts
from modules.logger import logger

bloggers = Blueprint(
    "bloggers", __name__, template_folder="templates", static_folder="static"
)


@bloggers.route("/bloggers")
def render_bloggers_page():
    try:
        users = Users.query.all()
        post_count_by_user = {}

        for user in users:
            post_count = len(user.blog_posts)
            post_count_by_user[user.id] = post_count

        return render_template(
            "bloggers.html", users_list=users, post_count_by_user=post_count_by_user
        )
    except Exception as e:
        logger.exception(f"Error rendering home page: {e}")

        return render_template("error.html", error=e)
