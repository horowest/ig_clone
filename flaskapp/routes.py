from flaskapp import app, db
from flask import render_template, redirect, url_for, flash, request
from flaskapp.forms import RegistrationForm, LoginForm, PostForm
from flaskapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required



@app.route("/")
def home():
    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template("home.html", title="FlaskApp", posts=posts)



@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
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

            next_page = request.args.get('next')

            return redirect(next_page or url_for('home'))
        else:
            flash("username or password is incorrect", 'danger')
            return redirect(url_for('login'))
    return render_template("login.html", title="Login", form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Posted successfully", 'success')
        return redirect(url_for('home'))
    return render_template("new_post.html", title="Post", form=form)