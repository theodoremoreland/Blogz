from . import db


class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    entry = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __init__(self, title, entry, author):
        self.title = title
        self.entry = entry
        self.author = author


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blog_posts = db.relationship(
        "BlogPosts", backref="author"
    )  # refers to name of model / class not table

    def __init__(self, username, password):
        self.username = username
        self.password = password
