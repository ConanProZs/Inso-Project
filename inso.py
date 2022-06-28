#wellcome to inso
from flask import Flask, render_template, session, url_for, request, redirect
from os import urandom
import json


def get_secret():
    file = open("data.json", "r")
    data = json.load(file)
    file.close()
    return data


app = Flask(__name__)
##################################
app.config["SECRET_KEY"] = urandom(125)
#login page
@app.route("/", methods = ['POST', 'GET'])
def login():
    session.clear()
    if request.method == 'POST':
        session['password'] = request.form['password']
        return redirect(url_for('home'))

    try:
        return render_template('login.html', errorinfo = request.args['errorinfo'])
    except:
        return render_template('login.html')

#home page
@app.route("/in/home")
def home():
    data = get_secret()
    if session.get('password') == data['password']:
        return render_template('home.html',)
    #if password is wrong or not set
    elif session.get('password') == None:
        return redirect(url_for('login'))
    elif session.get('password') != data['password']:
        errorinfo = "*Wrong password"
        return redirect(url_for('login', errorinfo=errorinfo))




##################################
#if page is not found
@app.errorhandler(404)
def page_not_found(e):
    errorinfo = "*Page not found"
    return redirect(url_for('login', errorinfo=errorinfo))
##################################
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False)