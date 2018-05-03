from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:bproductive@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'dsovnsovnzqrsB'






class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    entry = db.Column(db.String(1000))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, entry, author):
        self.title = title
        self.entry = entry
        self.author = author


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(20))
    blogs = db.relationship('Blog', backref='author')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'userblog', 'singleUser']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')
    




@app.route('/signup', methods=['POST', 'GET'])
def signup():
     if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify-password']

        if username == "":
            return render_template('signup.html', username_error="Field can not be empty")
        if len(username) <= 2 or len(username) > 20:
            return render_template('signup.html', username_error="Username is out of range 3-20")
        if username.count(" ") > 0:
            return render_template('signup.html', username_error="Username can not have spaces")
        if password == "":
            return render_template('signup.html', password_error="Fields can not be empty")
        if len(password) <= 2 or len(password) > 20:
            return render_template('signup.html', password_error="Password is out of range 3-20")
        if password.count(" ") > 0:
            return render_template('signup.html', password_error="Password can not have spaces")
        if password != verify:
            return render_template('signup.html', password_error="Passwords do not match",
            verify_error="Passwords do not match")

        else:
            existing_user = User.query.filter_by(username=username).first()
            
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                flash('You now have a Blogz user account')
                return redirect('/')
            else:
                flash('Username already in use')
                return render_template('signup.html', username_error="", password_error="",
                verify_error="")

     return render_template('signup.html', username_error="", password_error="",
     verify_error="")


@app.route('/')
def index():
        users = User.query.all()

         
        user_id = request.args.get("id")

        if user_id:
            blog = Blog.query_filter_by(author_id=user_id).all()
        
            return render_template("user.html", blogs=blog)

        return render_template('index.html', users_list=users)


    



@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')
    return render_template('login.html')



@app.route('/logout')
def logout():
    del session['username']
    flash("You are now logged out")
    return redirect('/')


@app.route('/blog')
def userblog():

 
    blog_id = request.args.get("id")
    user = request.args.get("user")

    if user:
       blog = Blog.query.filter_by(author_id=user).all()
    
       return render_template("user.html", blogs=blog)

    if blog_id:
        blog = Blog.query.filter_by(id=blog_id).all()

    else:
        blog = Blog.query.all()

    return render_template("blog.html", blogs=blog)



@app.route('/newpost', methods=['POST', 'GET'])
def new_post():

    author = User.query.filter_by(username=session['username']).first()

    if request.method == 'POST':
        entry = request.form['entry']
        title = request.form['title']
        if title == "" or entry == "":
            flash('Please fill both fields')
        else:
            blog = Blog(title, entry, author)
            db.session.add(blog)
            db.session.commit()
            blogs = Blog.query.all()
            blog_id = len(blogs)

        
            return redirect("/blog?id=" + str(blog_id))
    

    return render_template('newpost.html')



        



if __name__ == '__main__':
    app.run()