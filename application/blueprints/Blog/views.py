from flask import Blueprint, render_template, request, redirect, session, flash

from ...models import BlogPosts

blog = Blueprint(
    'blog',
    __name__, 
    template_folder='templates',
    static_folder='static'
    )

@blog.route('/blog')
def render_blog():
    blog_id = request.args.get("id")
    user = request.args.get("user")

    if user:
       _blog = BlogPosts.query.filter_by(author_id=user).all()
    elif blog_id:
        _blog = BlogPosts.query.filter_by(id=blog_id).all()
    else:
        _blog = BlogPosts.query.all()

    return render_template("blog.html", blog=_blog)