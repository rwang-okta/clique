import os
from flask import Flask, request, render_template, url_for, flash, session, redirect
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from database import db_session, init_db
from models import User, Creds

# from flask.ext.login import LoginManager

app = Flask(__name__)

#login init stuff.
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/home', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = valid_login(request.form['username'], request.form['password'])
        if user:
            login_user(user)
            session['username'] = request.form['username']
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
    creds = Creds.query.all()
    return render_template('cred.html', creds=creds)


#helpers
def valid_login(username, password):
    user = User.query.filter(User.email == username, User.password == password).first()
    return user

@login_manager.user_loader
def load_user(email):
    #print 'this is executed',userid
    return User(email)

def load_dummy_data():
    u = User('admin@okta.com', 'everychanceiget')
    db_session.add(u)
    u = User('rwang@okta.com', 'rayisawesome')
    db_session.add(u)
    c = Creds('Hipchat', '', 'rwang@okta.com')
    db_session.add(c)
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))
    db_session.add(Creds('blah', '', 'blah'))

    db_session.commit()


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
         load_dummy_data()

    app.run(debug=True)
