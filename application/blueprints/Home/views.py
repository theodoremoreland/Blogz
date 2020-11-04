from flask import Blueprint, render_template, Flask, request, redirect

from ...models import Users, BlogPosts

home = Blueprint(
    'home',
    __name__, 
    template_folder='templates',
    static_folder='static'
    )

@home.route('/')
def render_home_page():
    users = Users.query.all()
    user_id = request.args.get("id")

    if user_id:
        blog = BlogPosts.query_filter_by(author_id=user_id).all()
        return render_template("Blog/blog.html", blog=blog)

    return render_template('home.html', users_list=users)