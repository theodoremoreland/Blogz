from flask import Blueprint, render_template, request, redirect, session, flash

from ...models import db, Users

signup = Blueprint(
    'signup',
    __name__, 
    template_folder='templates',
    static_folder='static'
    )

@signup.route('/signup', methods=['POST', 'GET'])
def render_signup_page():
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
            existing_user = Users.query.filter_by(username=username).first()
            
            if not existing_user:
                new_user = Users(username, password)
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