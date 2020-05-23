from flaskapp import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from flaskapp.forms import RegistrationForm, LoginForm, PostForm, AccountUpdateForm
from flaskapp.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.utils import save_picture, save_media



@app.route("/")
def home():
    posts = current_user.get_followed_posts()

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
        media = save_media(form.media.data, 'media')
        post = Post(content=form.content.data, media=media, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Posted successfully", 'success')
        return redirect(url_for('home'))
    return render_template("new_post.html", title="Post", form=form)



@app.route("/user/<string:username>")
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    posts.reverse()
    return render_template("user.html", title=user.username, posts=posts, user=user)



@app.route("/post/")
def get_post():
    post_id = request.args.get('id')
    post = Post.query.get_or_404(int(post_id))

    return render_template("post.html", post=post) 



@app.route("/post/<int:post_id>/delete") 
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted", 'success')
        return redirect(url_for('home'))
    else:
        flash("You don't have delete priviledge for that post!", 'danger')
        return redirect(url_for('home'))



@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = AccountUpdateForm()
    
    if form.validate_on_submit():
        current_user.image_file = save_picture(form.picture.data, 'pfp')
        current_user.username = form.username.data
        db.session.commit()
        flash("Account infoo updated", 'success')
        return redirect(url_for('account'))
    # pre populate form
    if request.method == 'GET':
        form.username.data = current_user.username
        
    return render_template("account.html", title=current_user.username, form = form, image_url=current_user.image_file)



@app.route("/follow", methods=['GET', 'POST'])
@login_required
def follow_user():
    # user_id = int(request.args.get('id'))
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    current_user.follow(user)
    db.session.commit()
    # flash(f"You are now following {username}", 'success')

    return jsonify(result=username + " followed")
    # return redirect(url_for('get_user', username=user.username))



@app.route("/unfollow", methods=['GET', 'POST'])
@login_required
def unfollow_user():
    # user_id = int(request.args.get('id'))
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    current_user.unfollow(user)
    db.session.commit()
    # flash(f"{username} unfollowed", 'success')

    return jsonify(result=username + " unfollowed")
    # return redirect(url_for('get_user', username=user.username))