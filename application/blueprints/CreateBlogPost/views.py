from flask import Blueprint, render_template, request, redirect, session, flash

from ...models import db, Users, BlogPosts

create_blog_post = Blueprint(
    'create_blog_post',
    __name__, 
    template_folder='templates',
    static_folder='static'
    )


@create_blog_post.before_request
def require_login():
    if 'username' not in session:
        return redirect('/login')


@create_blog_post.route('/create-blog-post', methods=['POST', 'GET'])
def create_post():
    author = Users.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        entry = request.form['entry']
        title = request.form['title']

        if title == "" or entry == "":
            flash('Please fill both fields')
        else:
            blog_post = BlogPosts(title, entry, author)
            db.session.add(blog_post)
            db.session.commit()
            blog_posts = BlogPosts.query.all()
            blog_post_id = len(blog_posts)

            return redirect("/blog?id=" + str(blog_post_id))
    
    return render_template('create-blog-post.html')