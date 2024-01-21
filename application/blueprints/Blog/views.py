from flask import Blueprint, render_template, request, redirect, session, flash

from db import db
from db.models import BlogPosts, Users, Comments
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
            user = Users.query.filter_by(id=user_id).first()

            return render_template("blog.html", blog=user_blog, scope="user", user=user)
        elif blog_post_id:
            blog_post = BlogPosts.query.filter_by(id=blog_post_id).first()
            comments = blog_post.comments
            author_id = str(blog_post.author_id)
            user_id_in_session = str(session.get("user_id"))

            logger.info(
                f"Rendering blog post with blog_post_id: {blog_post_id} and author_id: {author_id} as user_id: {user_id_in_session}"
            )

            return render_template(
                "blog_post.html",
                blog_post=blog_post,
                comments=comments,
                is_owner=author_id == user_id_in_session,
            )
        else:
            all_blog_posts = BlogPosts.query.all()

            return render_template("blog.html", blog=all_blog_posts, scope="all")
    except Exception as e:
        logger.exception(f"Error rendering blog page: {e}")

        return render_template("error.html")


@blog.route("/delete-blog-post", methods=["POST"])
def delete_blog_post():
    blog_post_id = request.args.get("blog_post_id")

    try:
        user_id_in_session = session.get("user_id")
        blog_post = BlogPosts.query.filter_by(id=blog_post_id).first()

        if blog_post.author_id == user_id_in_session:
            db.session.delete(blog_post)
            db.session.commit()
        else:
            logger.info(
                f"User {user_id_in_session} attempted to delete blog post {blog_post_id} without permission"
            )

            flash("You do not have permission to delete this post", "error")

        return redirect("/blog")
    except Exception as e:
        logger.exception(f"Error deleting blog post: {e}")

        return render_template("error.html")


@blog.route("/comment", methods=["POST"])
def add_comment():
    if "username" not in session:
        logger.info("User not logged in, redirecting to login page")

        flash("You must be logged in to comment")

        return redirect("/login")

    comment = request.form.get("comment")
    blog_post_id = request.args.get("blog_post_id")
    author_id = session.get("user_id")

    try:
        if len(comment) < 5:
            comment_error = "Comment must be at least 5 characters long"
            logger.info("Comment has less than 5 characters, redirecting to blog post")

            flash(comment_error, "error")

            return redirect(f"/blog?blog_post_id={blog_post_id}")

        new_comment = Comments(
            comment=comment, blog_post_id=blog_post_id, author_id=author_id
        )
        db.session.add(new_comment)
        db.session.commit()

        return redirect(f"/blog?blog_post_id={blog_post_id}")
    except Exception as e:
        logger.exception(f"Error adding comment: {e}")

        return render_template("error.html")
