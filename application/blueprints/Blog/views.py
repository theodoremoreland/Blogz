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


# TODO: Refactor. Too many if statements. not DRY enough considering the reuse of the same template values and references.
@blog.route("/edit-blog-post", methods=["POST", "GET"])
def handle_edit_blog_post():
    logger.info(f"Request method: {request.method} for edit blog post page")

    username = session.get("username")
    blog_post_id = request.args.get("blog_post_id")

    if username is None:
        logger.info("User is not logged in. Redirecting to login page...")
        flash("You must be logged in to edit posts")

        return redirect("/login")

    if blog_post_id is None:
        logger.info("Blog post not specified. Redirecting to home page...")
        flash("Blog post not specified")

        return redirect("/")

    try:
        target_blog_post = BlogPosts.query.filter_by(id=blog_post_id).first()

        if target_blog_post is None:
            logger.info("Blog post not found. Redirecting to home page...")
            flash("Blog post not found")

            return redirect("/")

        if request.method == "POST":
            title = request.form["title"].strip()
            entry = request.form["entry"].strip()
            action = request.form["action"]

            if action == "update":
                logger.info(
                    f"User: {username} attempting to update blog post: {target_blog_post.title}"
                )

                if len(title) > 60 or len(title) < 3:
                    return render_template(
                        "edit_blog_post.html",
                        blog_post_id=blog_post_id,
                        title=title,
                        entry=entry,
                        title_error="Title must be between 3 and 60 characters",
                        entry_error="",
                    )
                elif len(entry) > 5000 or len(entry) < 5:
                    return render_template(
                        "edit_blog_post.html",
                        blog_post_id=blog_post_id,
                        title=title,
                        entry=entry,
                        title_error="",
                        entry_error="Entry must be between 5 and 5000 characters",
                    )
                else:
                    target_blog_post.title = title
                    target_blog_post.entry = entry
                    db.session.commit()
                    flash("Blog post updated!")

                    return render_template(
                        "blog_post.html",
                        blog_post=target_blog_post,
                        comments=target_blog_post.comments,
                        is_owner=True,
                    )
            elif action == "delete":
                logger.info(
                    f"User: {username} attempting to delete blog post id: {target_blog_post.id}, title: {title}"
                )

                db.session.delete(target_blog_post)
                db.session.commit()

                logger.info(
                    f"User: {username} deleted blog post id: {target_blog_post.id}, title: {title}"
                )
                flash("Blog post deleted!")

                return redirect("/")
            else:
                logger.error(f"Action {action} not recognized")
                flash("Action not recognized")

                return redirect("/")

        # if request.method == "GET"
        return render_template(
            "edit_blog_post.html",
            blog_post_id=target_blog_post.id,
            title=target_blog_post.title,
            entry=target_blog_post.entry,
            title_error="",
            entry_error="",
        )
    except Exception as e:
        logger.exception(f"Error editing blog post: {e}")

        return render_template("error.html")


@blog.route("/comment", methods=["POST"])
def add_comment():
    if "username" not in session:
        logger.info("User not logged in, redirecting to login page")

        flash("You must be logged in to comment")

        return redirect("/login")

    comment = request.form.get("comment").strip()
    blog_post_id = request.args.get("blog_post_id")
    author_id = session.get("user_id")

    try:
        comments_count = Comments.query.count()

        if comments_count > 500:
            logger.info("Maximum number of comments reached")

            flash("Maximum number of comments reached for this demo")

            return redirect(f"/blog?blog_post_id={blog_post_id}")
        elif len(comment) < 5 or len(comment) > 1000:
            comment_error = "Comment must be between 5 and 1000 characters"
            logger.info(comment_error)

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
