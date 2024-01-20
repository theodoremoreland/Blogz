from flask import Blueprint, render_template, request, redirect, session, flash

from db.models import Users
from modules.logger import logger

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if "username" in session:
        logger.info("User already logged in, redirecting to home page")

        flash("You are already logged in")

        return redirect("/")

    if request.method == "POST":
        logger.info("User attempting to log in")

        username = request.form["username"]
        password = request.form["password"]
        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            session["username"] = username
            flash("You are now logged in")

            logger.info(f"User {username} logged in")

            return redirect("/")
        else:
            message = "Password incorrect or user does not exist"

            logger.info(f"User {username} failed to log in. {message}")
            flash("Password incorrect or user does not exist", "error")

    logger.info("Rendering login page")

    return render_template("login.html")


@auth.route("/logout", methods=["GET"])
def logout():
    try:
        if "username" in session:
            username = session["username"]

            logger.info(f"User {username} logging out...")

            del session["username"]

            flash("You are now logged out")

            logger.info(f"User {username} logged out")

            return redirect("/")
        else:
            logger.info("User not logged in, redirecting to login page")

            flash("You must log in before you can log out")

            return redirect("/login")
    except Exception as e:
        logger.exception(f"Error logging out: {e}")

        return render_template("error.html")
