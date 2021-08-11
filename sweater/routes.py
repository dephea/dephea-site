from flask import Flask, render_template, redirect, request, flash
from flask_login import login_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash


from sweater import app, db
from sweater.models import Message, User


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index', methods=['GET'])
@login_required
def index():
    try:
        messages = Message.query.all()
    except:
        return 'Error while trying to read messages'
    return render_template('index.html', messages=messages)

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/add_message', methods=['POST'])
@login_required
def add_message():
    text = request.form['text']

    db.session.add(Message(text))
    db.session.commit()

    return redirect('/index')


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)



            return redirect('/index')
        else:
            flash('Login or password incorrect')

    else:
        flash('Please fill login and password fields')

    return render_template('/login_page.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    if request.method == 'POST':
        if not(login or password or password2):
            flash('Please, fill all fields')
        elif password != password2:
            flash('Passwords are not the same')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect('/login_page')

    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout.user()
    return redirect('/home')


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect('/login_page' + '?next=' + request_url)

    return response