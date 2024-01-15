from flask import Blueprint, render_template, request, redirect, session, flash

from db.models import BlogPosts, Users
from modules.logger import logger

blog = Blueprint("blog", __name__, template_folder="templates", static_folder="static")


@blog.route("/blog", methods=["GET"])
def render_blog():
    user_id = request.args.get(
        "user"
    )  # assigned when a user clicks on a link to a user profile
    blog_post_id = request.args.get(
        "blog_post_id"
    )  # assigned when clicking on link to specific post or after creating post

    logger.info(
        f"Rendering blog page with user_id: {user_id} and blog_post_id: {blog_post_id}"
    )
    try:
        if user_id:
            user_blog = BlogPosts.query.filter_by(author_id=user_id).all()
            username = Users.query.filter_by(id=user_id).first().username
            return render_template(
                "blog.html", blog=user_blog, header=f"{username}'s Blog "
            )
        elif blog_post_id:
            blog_post = BlogPosts.query.filter_by(id=blog_post_id).first()
            return render_template("blog_post.html", blog_post=blog_post)
        else:
            all_blog_posts = BlogPosts.query.all()
            return render_template(
                "blog.html", blog=all_blog_posts, header=f"All Blog Posts"
            )
    except Exception as e:
        logger.exception(f"Error rendering blog page: {e}")

        return render_template("error.html", error=e)
