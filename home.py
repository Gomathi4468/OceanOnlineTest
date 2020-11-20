import pyrebase
from flask import Flask, render_template, request, flash,session,redirect,url_for,make_response
from firebase_admin import credentials, firestore, initialize_app
import re
import random, string
from forms import LoginForm,RegistrationForm


app = Flask(__name__)
app.config['SECRET_KEY'] = '1456780765656546'

firebaseConfig = {
    'apiKey': "AIzaSyDprWkumoIjc2zBN0j9Hp2ohfefU2nrv-o",
    'authDomain': "crudflask-be52c.firebaseapp.com",
    'databaseURL': "https://crudflask-be52c.firebaseio.com",
    'projectId': "crudflask-be52c",
    'storageBucket': "crudflask-be52c.appspot.com",
    'messagingSenderId': "60768817778",
    'appId': "1:60768817778:web:b5db1178bbde7604f128eb",
    'measurementId': "G-0WC9TEZ6W5"
  }


cred = credentials.Certificate("service.json")
default_app=initialize_app(cred)

db = firestore.client()
firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

@app.route("/home",methods=['GET', 'POST'])
def home():
    if 'email' in session:
        email = session['email']
        return render_template('home.html', name=email)
    else:
        return render_template('general.html')

@app.route("/",methods=['GET', 'POST'])
def general():
    return render_template('general.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        try:
            if auth.create_user_with_email_and_password(email, password):
                reg = db.collection('register').document(email)
                doc = {'username': username, 'email': email, }
                reg.set(doc)
                flash(f'Account created for {form.username.data}!', 'success')
                session['email'] = request.form['email']
                session['id'] = request.form['username']
                return redirect(url_for('home'))
            else:
                return render_template('register.html', title='Register', form=form)
        except:
            flash('Already exist', 'danger')
            return render_template('register.html', title='Register', form=form)
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        try:
            if auth.sign_in_with_email_and_password(email, password):
                print("1")
                reg = db.collection('register').document(email).get().to_dict()
                print(reg)
                session['email'] = request.form['email']
                session['id'] = reg['username']
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return render_template('login.html', title='Login', form=form)
        except:
            flash('Login Unsuccessful. Please check username and password', 'danger')
            return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)
@app.route('/logout')
def logout():
    session.clear()
    return render_template('general.html')

@app.route("/profile")
def profile():
    if 'email' in session:
        email = session['email']
        return render_template('profile.html', name=email)
    else:
        return render_template('general.html')


@app.route("/about")
def about():
    if 'email' in session:
        email = session['email']
        return render_template('about.html', name=email)
    else:
        return render_template('general.html')

@app.route("/forgot")
def forgot():
        return render_template('forgot.html')

@app.route("/reset", methods=["GET","POST"])
def reset():
    email=request.form['reset']
    auth.send_password_reset_email(email)
    return "password changed successfully"

@app.route("/test")
def test():
    if 'email' in session:
        email = session['email']
        return render_template('test.html', name=email)
    else:
        return render_template('general.html')

@app.route("/language")
def language():
    if 'email' in session:
        email = session['email']
        return render_template('language.html', name=email)
    else:
        return render_template('general.html')

@app.route("/pythontopics")
def pythontopics():
    top = db.collection("python")
    docs = top.get()
    a=[]
    for doc in docs:
       #print(doc.id)
        a.append(doc.id)
    print(a)
    return render_template('pythontest.html', new=a)


@app.route("/javatopics")
def javatopics():
    if 'email' in session:
        email = session['email']
        return render_template('javatest.html', name=email)
    else:
        return render_template('general.html')

@app.route("/ctopics")
def ctopics():
    if 'email' in session:
        email = session['email']
        return render_template('ctest.html', name=email)
    else:
        return render_template('general.html')

@app.route("/mcq", methods=['GET'])
def mcq():
    top = db.collection('python').document(session['title']).collection('mcq')
    docs = top.get()
    b = []
    for doc in docs:
        # print(doc.id)
       b.append(doc.id)
    print(b)
    x = request.args.get('x', None)
    if x:
        if 'email' in session:
            email = session['email']
            n = '1'
            if session.get("qid"):
                n = int(session["qid"]) + 1
            session["qid"] = n
            #print(n)
            doc_ref = db.collection('python').document(session['title']).collection('mcq').document(str(n))
            document = doc_ref.get()
            a = document.to_dict()
            if a:
            # print(a)
            # return render_template("mcq.html",new=a['qid'],new1=a['question'],new3=a['a'],new4=a['b'],new5=a['c'],new6=a['d'])
                return render_template("mcq.html", new=a, name=email,new1=b,title=session['title'])
            else:
                session["qid"] = "0"
                return render_template("pythontest.html")
        else:
            return render_template("general.html")

@app.route("/mcqq", methods=['GET'])
def mcqq():
    x = request.args.get('id', None)


    doc_ref = db.collection('question').document(str(x))
    document = doc_ref.get()
    a = document.to_dict()
    if a:
            # print(a)
            # return render_template("mcq.html",new=a['qid'],new1=a['question'],new3=a['a'],new4=a['b'],new5=a['c'],new6=a['d'])
        return render_template("mcq.html", new=a)
    else:
        session["qid"] = "0"
        return render_template("pythontest.html")



@app.route("/instruction")
def instruction():
    session['title']=request.args.get('x',None)
    if 'email' in session:
        email = session['email']
        return render_template('instruction.html', name=email)
    else:
        return render_template('general.html')




if __name__ == '__main__':
    app.run(debug=True)
