from flask import Blueprint, render_template, request, redirect, session, flash

from db.models import db, Users
from modules.logger import logger
from utils.validate_image_url import validate_image_url

edit_profile = Blueprint(
    "edit_profile", __name__, template_folder="templates", static_folder="static"
)


# TODO: Refactor. Too many if statements.
@edit_profile.route("/edit-profile", methods=["POST", "GET"])
def handle_edit_profile():
    logger.info(f"Rendering edit_profile page with request method: {request.method}")

    username = session.get("username")

    if username is None:
        logger.info("User is not logged in. Redirecting to login page...")
        flash("You must be logged in to edit your profile")

        return redirect("/login")

    try:
        existing_user = Users.query.filter_by(username=username).first()

        if existing_user is None:
            logger.info("User does not exist. Redirecting to login page...")
            flash("User not found. Please login again")

            return redirect("/login")

        if request.method == "POST":
            about_me = request.form["about-me"].strip()
            avatar_url = request.form["avatar-url"].strip()
            action = request.form["action"]

            if action == "update":
                logger.info(
                    f"User: {username} attempting to edit profile with about me: {about_me}"
                )

                if validate_image_url(avatar_url) == False:
                    return render_template(
                        "edit_profile.html",
                        avatar_url=avatar_url,
                        avatar_url_error="Invalid URL",
                    )

                if about_me == "":
                    return render_template(
                        "edit_profile.html",
                        about_me=about_me,
                        about_me_error="Field can not be empty",
                    )
                elif len(about_me) > 1000:
                    return render_template(
                        "edit_profile.html",
                        about_me=about_me,
                        about_me_error="About me cannot exceed 1000 characters",
                    )
                else:
                    existing_user.avatar_url = avatar_url
                    existing_user.about_me = about_me
                    db.session.commit()
                    flash("User profile updated!")

                    return render_template(
                        "edit_profile.html", about_me=about_me, about_me_error=""
                    )
            elif action == "delete":
                logger.info(f"User: {username} attempting to delete user profile...")

                db.session.delete(existing_user)
                db.session.commit()

                del session["username"]

                logger.info(f"User: {username} profile deleted")
                flash("User profile deleted!")

                return redirect("/")
            else:
                logger.error(f"Action {action} not recognized")
                flash("Action not recognized")

                return redirect("/")

        # if request.method == "GET"
        return render_template(
            "edit_profile.html",
            about_me=existing_user.about_me,
            avatar_url=existing_user.avatar_url,
            about_me_error="",
            avatar_url_error="",
        )
    except Exception as e:
        logger.exception(f"Error editing user profile: {e}")

        return render_template("error.html")
