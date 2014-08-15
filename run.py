import os
from flask import Flask, request, render_template, url_for, flash, session, redirect
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from database import db_session, init_db
from models import User

#from flask.ext.login import LoginManager

app = Flask(__name__)

#login init stuff.
login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/home', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        user = valid_login(request.form['username'], request.form['password'])
        if user:
            login_user(user)
            session['username'] = request.form['username']
            flash("logged in successfully.")
            return redirect('/cred')
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET','POST'])
def logout():
    error = None
    session.pop('username', None)
    return redirect('/login')

@login_required
@app.route('/cred', methods=['GET'])
def cred():
    return render_template('cred.html')


#helpers
def valid_login(username, password):
    user = User.query.filter(User.email == username, User.password == password).first()
    return user

@login_manager.user_loader
def load_user(email):
    #print 'this is executed',userid
    return User(email)

#tears down session connections when apps die.
#@app.teardown_appcontext
#def shutdown_session():
#    db_session.remove()

#application
if __name__ == '__main__':
    app.secret_key = 'cliquef1293189tma8345halkfnsuyb78abnio2h3kla'
    #we do this with gunicorn on prod servers, so only enable this locally for testing.

    init_db()

    #default user (may change this to only add a user if none currently exists)
    if not User.query.all():
        u = User('admin@okta.com', 'everychanceiget')
        db_session.add(u)
        db_session.commit()

    #app.run(debug = True)
