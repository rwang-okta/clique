import os
from flask import Flask, request, render_template, url_for
from flask_login import login_required, login_user, logout_user, current_user

#from flask.ext.login import LoginManager

app = Flask(__name__)

#login init stuff.
#login_manager = LoginManager()
#login_manager.init_app(app)

#@app.route('/')
#def hello():
#    return 'Hello World!'

@app.route('/home', methods=['GET'])
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
            request.form['password']):
            return render_template('cred.html', error=error)#log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

@app.route('/cred', methods=['GET'])
def cred():
    return render_template('cred.html')

#helpers
def valid_login(username, password):
    #TODO: make this an actual login
    if (username == "a@a.com" and password == "b"):
        return True;
    else:
        return False;

if __name__ == '__main__':
    app.secret_key = 'cliquef1293189tma8345halkfnsuyb78abnio2h3kla';
    #we do this with gunicorn on prod servers, so only enable this locally for testing.
    app.run(debug = True)
