from flask import Blueprint, render_template, request, redirect, session, flash

from ...models import Users

auth = Blueprint(
    'auth',
    __name__, 
    template_folder='templates',
    static_folder='static'
    )


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')
            
    return render_template('login.html')


@auth.route('/logout')
def logout():
    if 'username' not in session:
        return redirect('/login')
    del session['username']
    flash("You are now logged out")
    
    return redirect('/')