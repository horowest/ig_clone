from flaskapp import app, db
from flask import render_template, redirect, url_for, flash, request
from flaskapp.forms import RegistrationForm, LoginForm
from flaskapp.models import User
from flask_login import login_user, current_user, logout_user, login_required


posts = [
    {
        'author':'akash',
        'content':'This is a first post',
        'date_posted':'21 May, 2020'
    },
    {
        'author':'horowest',
        'content':'This is a second post',
        'date_posted':'21 May, 2020'
    }
]



@app.route("/")
def home():
    return render_template("home.html", title="FlaskApp", posts=posts)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Account registerd sucessfully. You can now login", 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title="Register", form=form)



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash("You have been logged in successfully", 'success')
            return redirect(url_for('home'))
        else:
            flash("username or password is incorrect", 'danger')
            return redirect(url_for('login'))
    return render_template("login.html", title="Login", form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    