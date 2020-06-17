from flaskapp import app, db
from flask import render_template, redirect, url_for, flash, request, jsonify
from flaskapp.forms import RegistrationForm, LoginForm, PostForm, AccountUpdateForm, CommentPostForm
from flaskapp.models import User, Post, Comment, Notif
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.utils import save_picture, save_media, get_file_url, delete_file


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return redirect(url_for('register'))
        return render_template("home.html", title="Instaclone", get_file_url=get_file_url)


    if request.method == 'POST':
        start = int(request.form.get('start') or 1)
        # get posts
        posts = current_user.get_followed_posts().paginate(start, 2, False).items

        result = []
        for post in posts:
            # print(post.pid)

            comments = []
            for comment in post.get_comments(limit=2):
                comments.append(
                    {    
                        'cid': comment.cid,
                        'content': comment.content,
                        'post_id': comment.post_id,
                        'author': 
                        {   
                            'uid': comment.author.uid,
                            'username': comment.author.username,
                            'image_file': get_file_url('profile_pics/' + comment.author.image_file),
                            'user_url': url_for('get_user', username=comment.author.username)
                        }
                    }
                )

            result.append(
                {
                    'pid': post.pid,
                    'content': post.content,
                    'media': get_file_url('media/' + post.media),
                    'date_posted': post.date_posted,
                    'post_url': url_for('get_post', post_id=post.pid),
                    'liked': post.user_liked(current_user),
                    'like_count': post.get_likes_count(),
                    'timeago': post.get_timeago(),
                    'author': 
                    {   
                        'uid': post.author.uid,
                        'username': post.author.username,
                        'image_file': get_file_url('profile_pics/' + post.author.image_file),
                        'user_url': url_for('get_user', username=post.author.username)
                    },
                    'comment_count': post.comments_count(),
                    'comments': comments
                }
            )
        status = True
        return jsonify(result=result, success=status)


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
    return redirect(url_for('register'))



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
    return render_template("new_post.html", title="Instaclone", form=form, get_file_url=get_file_url)



@app.route("/user/<string:username>")
def get_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = user.posts
    posts.reverse()
    return render_template("user.html", title=user.username, posts=posts, user=user, get_file_url=get_file_url)



@app.route("/post/id/<int:post_id>")
def get_post(post_id):
    # post_id = request.args.get('post_id')
    post = Post.query.get_or_404(int(post_id))

    return render_template("post.html", title="Instaclone", post=post, get_file_url=get_file_url)



@app.route("/post/<int:post_id>/delete")
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author == current_user:
        db.session.query(Comment).filter(Comment.post_id == post.pid).delete()
        db.session.query(Notif).filter(Notif.post_id == post.pid).delete()
        delete_file(post.media)
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
        flash("Account updated", 'success')
        return redirect(url_for('account'))
    # pre populate form
    if request.method == 'GET':
        form.username.data = current_user.username

    return render_template("account.html", title='Account',
                            form = form, image_url=current_user.image_file, get_file_url=get_file_url)



@app.route("/follow", methods=['GET', 'POST'])
@login_required
def follow_user():
    # user_id = int(request.args.get('id'))
    if request.method == 'GET':
        username = request.args.get('username')
    else:
        username = request.form['username']
    print(username)
    user = User.query.filter_by(username=username).first()
    current_user.follow(user)
    db.session.commit()
    # flash(f"You are now following {username}", 'success')

    return jsonify(result=username + " followed")
    # return redirect(url_for('get_user', username=user.username))



@app.route("/unfollow", methods=['POST'])
@login_required
def unfollow_user():
    # user_id = int(request.args.get('id'))
    username = request.form['username']
    user = User.query.filter_by(username=username).first()
    current_user.unfollow(user)
    db.session.commit()
    print(username)
    # flash(f"{username} unfollowed", 'success')

    return jsonify(result=username + " unfollowed")
    # return redirect(url_for('get_user', username=user.username))


@app.route("/post/<int:post_id>/like", methods=['GET', 'POST'])
@login_required
def post_likes(post_id):
    post = Post.query.get(int(post_id))
    r = post.like_post(current_user)

    # notify
    if post.author != current_user:
        if r == "like":
            n = Notif.add_notif(current_user, post, 'liked')
            db.session.add(n)

    db.session.commit()
    return jsonify(result=post.get_likes_count())



@app.route("/comment/<int:post_id>", methods=['POST'])
@login_required
def make_comment(post_id):
    content = request.form['msg']
    post = Post.query.get(int(post_id))
    if post:
        c = Comment(content=content, author=current_user, post_id=post_id)
        db.session.add(c)

        # notify
        if post.author != current_user:
            n = Notif.add_notif(current_user, post, 'commented on')
            db.session.add(n)

        db.session.commit()

        return jsonify(username=current_user.username,
                    user_url=url_for('get_user', username=current_user.username),
                    content=content, cid=c.cid, date_posted=c.date_posted.strftime('%d-%m-%Y'))



@app.route("/comment/<int:com_id>/delete")
@login_required
def delete_comment(com_id):
    com = Comment.query.get_or_404(com_id)
    # print(com, com.author, current_user)
    if com.author == current_user:
        db.session.delete(com)
        db.session.commit()

    return jsonify(result='')


@app.route("/explore", methods=['GET', 'POST'])
def explore():
    if request.method == 'GET':
        if not current_user.is_authenticated:
            return redirect(url_for('register'))
        return render_template("explore.html", title="Explore", get_file_url=get_file_url)


    if request.method == 'POST':
        start = int(request.form.get('start') or 1)
        # get posts
        posts = Post.query.paginate(start, 3, False).items

        result = []
        for post in posts:
            # print(post.pid)

            result.append(
                {
                    'media': get_file_url('media/mid' + post.media),
                    'post_url': url_for('get_post', post_id=post.pid),
                }
            )
        status = True
        return jsonify(result=result, success=status)
