import os, re, datetime
from flask import Flask, request, render_template, url_for, flash, session, redirect
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from database import db_session, init_db
from models import User, Creds, CredsSerializer
from marshmallow import pprint

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
@app.route('/cred', methods=['GET', 'POST'])
def cred():
    if request.method == 'POST':
        add_credential(request.form['name'], request.form['loginurl'], request.form['username'],
                       request.form['password'], request.form['notes'], request.form['checkout'],
                       request.form['expireon'])
    creds = Creds.query.all()
    return render_template('cred.html', creds=creds)


@login_required
@app.route('/cred-remove', methods=['GET'])
def cred_remove():
    creds = Creds.query.all()
    return render_template('cred-remove.html', creds=creds)


@login_required
@app.route('/cred-remove/<int:credId>', methods=['POST'])
def remove_cred(credId):
    get_credentials = Creds.query.filter(Creds.id == int(credId)).first()
    db_session.delete(get_credentials)
    db_session.commit()
    creds = Creds.query.all()
    return render_template('cred.html', creds=creds)


#not restful, should combine it with the previous function, but something we cna fix later.
@login_required
@app.route('/cred/<int:credId>', methods=['GET', 'POST'])
def get_cred(credId):
    if request.method == 'GET':
        get_credentials = Creds.query.filter(Creds.id == int(credId)).first()

        serialized = CredsSerializer(get_credentials)
        return serialized.json
    else:
        get_credentials = Creds.query.filter(Creds.id == int(credId)).first()
        get_credentials.user = session['username']
        db_session.commit()
        creds = Creds.query.all()
        return render_template('cred.html', creds=creds)
        #return redirect('/cred')


def add_credential(oam_app_name, loginurl, username, password, comment, checkout, expire):
    db_session.add(Creds(oam_app_name, comment, None, loginurl, username, password,
                         datetime.datetime.strptime(checkout, "%m-%d-%y"),
                         datetime.datetime.strptime(expire, "%m-%d-%y")))
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
    db_session.add(Creds('Concur', 'For Sales use only.', 'sshen@okta.com', None, None, None,
                         datetime.datetime.strptime("07-18-14", "%m-%d-%y"), datetime.datetime.strptime("08-21-14", "%m-%d-%y")))
    db_session.add(Creds('Concur', '', 'bng@okta.com', None, None, None,
                         datetime.datetime.strptime("08-18-14", "%m-%d-%y"), datetime.datetime.strptime("08-21-14", "%m-%d-%y")))
    db_session.add(Creds('Concur', '', None, 'http://www.concur.com/login', 'abc@concur.com', 'OktaOktaOkta12345',
                         datetime.datetime.strptime("08-13-14", "%m-%d-%y"), datetime.datetime.strptime("09-21-14", "%m-%d-%y")))
    db_session.add(Creds('O365', '', None, 'http://www.office.com/login', 'abc@office.com', 'password12',
                         datetime.datetime.strptime("08-15-14", "%m-%d-%y"), datetime.datetime.strptime("08-21-14", "%m-%d-%y")))
    db_session.add(Creds('O365', 'Compromised!', 'Disabled', None, None, None,
                         datetime.datetime.strptime("08-18-14", "%m-%d-%y"), datetime.datetime.strptime("08-21-14", "%m-%d-%y")))
    db_session.add(Creds('O365', '', None, 'http://www.oficce.com/login', 'abc@office.com', 'nopasswordhere.',
                         datetime.datetime.strptime("08-10-14", "%m-%d-%y"), datetime.datetime.strptime("08-19-14", "%m-%d-%y")))
    db_session.add(Creds('Coupa', '', None, None, None, None,
                         datetime.datetime.strptime("08-18-14", "%m-%d-%y"), datetime.datetime.strptime("08-23-14", "%m-%d-%y")))
    db_session.add(Creds('Coupa', '', None, None, None, None,
                         datetime.datetime.strptime("08-18-14", "%m-%d-%y"), datetime.datetime.strptime("08-31-14", "%m-%d-%y")))
    db_session.add(Creds('ServiceNow', '', 'Disabled', None, None, None,
                         datetime.datetime.strptime("08-13-14", "%m-%d-%y"), datetime.datetime.strptime("08-17-14", "%m-%d-%y")))
    db_session.add(Creds('ServiceNow', '', None, None, None, None,
                         datetime.datetime.strptime("07-18-14", "%m-%d-%y"), datetime.datetime.strptime("08-21-14", "%m-%d-%y")))
    db_session.add(Creds('Jobvite', '', None, None, None, None,
                         datetime.datetime.strptime("08-18-14", "%m-%d-%y"), datetime.datetime.strptime("08-25-14", "%m-%d-%y")))
    db_session.add(Creds('Salesforce', '', None, None, None, None,
                         datetime.datetime.strptime("07-29-14", "%m-%d-%y"), datetime.datetime.strptime("08-27-14", "%m-%d-%y")))
    db_session.add(Creds('Salesforce', '', 'Disabled', None, None, None,
                         datetime.datetime.strptime("07-18-14", "%m-%d-%y"), datetime.datetime.strptime("08-20-14", "%m-%d-%y")))
    db_session.add(Creds('Salesforce', '', None, None, None, None,
                         datetime.datetime.strptime("07-21-14", "%m-%d-%y"), datetime.datetime.strptime("09-10-14", "%m-%d-%y")))
    db_session.add(Creds('Salesforce', '', 'jackychen@okta.com', None, None, None,
                         datetime.datetime.strptime("08-10-14", "%m-%d-%y"), datetime.datetime.strptime("09-03-14", "%m-%d-%y")))
    db_session.add(Creds('WebEx', '', None, None, None, None,
                         datetime.datetime.strptime("08-03-14", "%m-%d-%y"), datetime.datetime.strptime("08-23-14", "%m-%d-%y")))
    db_session.add(Creds('Workday', 'For Eng use only.', 'cwu@okta.com', None, None, None,
                         datetime.datetime.strptime("08-10-14", "%m-%d-%y"), datetime.datetime.strptime("08-21-14", "%m-%d-%y")))
    db_session.add(Creds('Workday', 'For Sales use only.', 'rwang@okta.com', None, None, None,
                         datetime.datetime.strptime("08-05-14", "%m-%d-%y"), datetime.datetime.strptime("08-25-14", "%m-%d-%y")))

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
