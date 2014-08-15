import os
from flask import Flask, request, render_template, url_for
#from flask.ext.login import LoginManager

app = Flask(__name__)

#login init stuff.
#login_manager = LoginManager()
#login_manager.init_app(app)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/login', methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'],
            request.form['password']):
            return render_template('home.html', error=error)#log_the_user_in(request.form['username'])
    else:
        error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

#helpers
def valid_login(username, password):
    #TODO: make this an actual login
    if (username == "a" and password == "b"):
        return True;
    else:
        return False;

#app.secret_key = 'cliquef1293189tma8345halkfnsuyb78abnio2h3kla';

app.run(debug = True)
