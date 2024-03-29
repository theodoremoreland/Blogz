from flask import Blueprint, render_template, request, redirect, session, flash
import bcrypt

from db.models import db, Users
from modules.logger import logger
from utils.validate_image_url import validate_image_url

signup = Blueprint(
    "signup", __name__, template_folder="templates", static_folder="static"
)


@signup.route("/signup", methods=["POST", "GET"])
def render_signup_page():
    logger.info(f"Rendering signup page with request method: {request.method}")

    if "username" in session:
        logger.info("User already has an account. Redirecting to home page...")
        flash("You already have an account")

        return redirect("/")

    if request.method == "POST":
        try:
            username = request.form["username"].strip()
            password = request.form["password"]
            verify = request.form["verify-password"]
            avatar_url = request.form["avatar-url"].strip()
            about_me = request.form["about-me"].strip()

            logger.info(
                f"User attempting to sign up as {username}, with about me: {about_me}"
            )

            if username == "":
                return render_template(
                    "signup.html", username_error="Field can not be empty"
                )

            if len(username) <= 2 or len(username) > 20:
                return render_template(
                    "signup.html", username_error="Username is out of range 3-20"
                )

            if username.count(" ") > 0:
                return render_template(
                    "signup.html", username_error="Username can not have spaces"
                )

            if password == "":
                return render_template(
                    "signup.html", password_error="Fields can not be empty"
                )

            if len(password) <= 2 or len(password) > 20:
                return render_template(
                    "signup.html", password_error="Password is out of range 3-20"
                )

            if password.count(" ") > 0:
                return render_template(
                    "signup.html", password_error="Password can not have spaces"
                )

            if password != verify:
                return render_template(
                    "signup.html",
                    password_error="Passwords do not match",
                    verify_error="Passwords do not match",
                )

            if validate_image_url(avatar_url) == False:
                return render_template("signup.html", avatar_url_error="Invalid URL")

            if about_me == "":
                return render_template(
                    "signup.html", about_me_error="Field can not be empty"
                )

            if len(about_me) > 1000:
                return render_template(
                    "signup.html",
                    about_me_error="About me cannot exceed 1000 characters",
                )

            else:
                existing_user = Users.query.filter_by(username=username).first()

                if Users.query.count() > 50:
                    flash(
                        "Unable to create new user. The maximum number of users for this demo has been reached."
                    )

                    return redirect("/")
                elif not existing_user:
                    password_bytes = password.encode("utf-8")
                    salt = bcrypt.gensalt()
                    password_hash = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

                    new_user = Users(username, password_hash, about_me, avatar_url)

                    db.session.add(new_user)
                    db.session.commit()

                    session["username"] = username
                    session["user_id"] = new_user.id
                    flash("blogz user account created!")

                    return redirect("/")
                else:
                    flash("Username already in use")

                    return render_template(
                        "signup.html",
                        username_error="",
                        password_error="",
                        verify_error="",
                    )
        except Exception as e:
            logger.exception(f"Error rendering signup page: {e}")

            return render_template("error.html", error=e)

    return render_template(
        "signup.html", username_error="", password_error="", verify_error=""
    )
