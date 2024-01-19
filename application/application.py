# Third party
from flask import Flask

# Models
from db import db

# Blueprints
from blueprints.Auth.views import auth
from blueprints.Blog.views import blog
from blueprints.Bloggers.views import bloggers
from blueprints.CreateBlogPost.views import create_blog_post
from blueprints.Root.views import root
from blueprints.SignUp.views import signup


application = Flask(__name__, instance_relative_config=True)
application.config.from_pyfile("config.cfg")
application.config.from_pyfile("../config.py")
application.register_blueprint(auth)
application.register_blueprint(blog)
application.register_blueprint(bloggers)
application.register_blueprint(create_blog_post)
application.register_blueprint(root)
application.register_blueprint(signup)

db.init_app(application)

with application.app_context():
    db.create_all()

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
