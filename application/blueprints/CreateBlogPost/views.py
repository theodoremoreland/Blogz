from flask import Blueprint, render_template, request, redirect, session, flash

from db.models import db, Users, BlogPosts
from modules.logger import logger

create_blog_post = Blueprint(
    "create_blog_post", __name__, template_folder="templates", static_folder="static"
)


@create_blog_post.before_request
def require_login():
    if "username" not in session:
        logger.info("User not logged in, redirecting to login page")

        return redirect("/login")


@create_blog_post.route("/create-blog-post", methods=["POST", "GET"])
def create_post():
    try:
        if request.method == "POST":
            logger.info(f"Creating blog post")

            entry = request.form["entry"]
            title = request.form["title"]

            if title == "" or entry == "":
                flash("Please fill both fields")
            else:
                author = Users.query.filter_by(username=session["username"]).first()
                blog_post = BlogPosts(title, entry, author)

                db.session.add(blog_post)
                db.session.commit()

                blog_post_id = (
                    BlogPosts.query.filter_by(title=title, entry=entry).first().id
                )

                flash("Blog post created")

                return redirect("/blog?blog_post_id=" + str(blog_post_id))

        logger.info(f"Rendering create blog post page")

        return render_template("create_blog_post.html")
    except Exception as e:
        logger.exception(f"Error handling blog post request: {e}")

        return render_template("error.html")
