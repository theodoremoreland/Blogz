from . import db


class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    entry = db.Column(db.String(5000))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    comments = db.relationship("Comments", backref="blog_post")

    def __init__(self, title, entry, author):
        self.title = title
        self.entry = entry
        self.author = author


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(100))
    about_me = db.Column(db.String(1000))
    avatar_url = db.Column(db.String(160))
    member_since = db.Column(db.DateTime, server_default=db.func.now())
    blog_posts = db.relationship(
        "BlogPosts", backref="author"
    )  # refers to name of model / class not table
    comments = db.relationship("Comments", backref="author")

    def __init__(self, username, password, about_me, avatar_url):
        self.username = username
        self.password = password
        self.about_me = about_me
        self.avatar_url = avatar_url


class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    blog_post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __init__(self, comment, author_id, blog_post_id):
        self.comment = comment
        self.author_id = author_id
        self.blog_post_id = blog_post_id
