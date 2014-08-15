import os, re
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

@app.route('/join', methods=['GET', 'POST'])
def join():
    error = None
    joined = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #TODO better ways for regex?
        domain = re.search("@[\w.]+", username)
        if domain.group() == '@okta.com':
            db_session.add(User(username, password))
            db_session.commit()
            joined = True
        else:
            error = 'Only Okta users can join the Clique :)'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('join.html', error=error, joined=joined)

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


def add_credential(oam_app_name, comment, checkout, expire):
    db_session.add(Creds(oam_app_name, comment, None, checkout, expire))
    db_session.commit()


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
    db_session.add(Creds('Concur', '', 'sshen@okta.com'))
    db_session.add(Creds('Concur', '', 'bng@okta.com'))
    db_session.add(Creds('Concur', '', None))
    db_session.add(Creds('O365', '', None))
    db_session.add(Creds('O365', '', 'Disabled'))
    db_session.add(Creds('O365', '', None))
    db_session.add(Creds('Coupa', '', None))
    db_session.add(Creds('Coupa', '', None))
    db_session.add(Creds('ServiceNow', '', 'Disabled'))
    db_session.add(Creds('ServiceNow', '', None))
    db_session.add(Creds('Jobvite', '', None))
    db_session.add(Creds('Salesforce', '', None))
    db_session.add(Creds('Salesforce', '', 'Disabled'))
    db_session.add(Creds('Salesforce', '', None))
    db_session.add(Creds('Salesforce', '', 'jackychen@okta.com'))
    db_session.add(Creds('WebEx', '', None))
    db_session.add(Creds('Workday', 'For Eng use only.', 'cwu@okta.com'))
    db_session.add(Creds('Workday', 'For Sales use only.', 'rwang@okta.com'))

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
