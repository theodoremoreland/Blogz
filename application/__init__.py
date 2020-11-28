# Third party
from flask import Flask, redirect, request, session
from flask_sqlalchemy import SQLAlchemy

# Models
from .models import db
from .models import Users, BlogPosts

# Blueprints
from .blueprints.Auth.views import auth
from .blueprints.Blog.views import blog
from .blueprints.CreateBlogPost.views import create_blog_post
from .blueprints.Home.views import home
from .blueprints.SignUp.views import signup


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.register_blueprint(auth)
app.register_blueprint(blog)
app.register_blueprint(create_blog_post)
app.register_blueprint(home)
app.register_blueprint(signup)
db.init_app(app)


# @app.before_first_request
# def require_login():
#     Users.__table__.create(db.engine)
#     BlogPosts.__table__.create(db.engine)
