from flask import Blueprint, render_template, request, redirect, session, flash

from db.models import db, Users
from modules.logger import logger

signup = Blueprint(
    "signup", __name__, template_folder="templates", static_folder="static"
)


@signup.route("/signup", methods=["POST", "GET"])
def render_signup_page():
    logger.info(f"Rendering signup page with request method: {request.method}")

    if request.method == "POST":
        try:
            username = request.form["username"]
            password = request.form["password"]
            verify = request.form["verify-password"]
            about_me = request.form["about-me"]

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

            else:
                existing_user = Users.query.filter_by(username=username).first()

                if not existing_user:
                    new_user = Users(username, password, about_me)
                    db.session.add(new_user)
                    db.session.commit()
                    session["username"] = username
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
