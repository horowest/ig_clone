from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin

# User 
# uid int
# username string
# password string
# image_file string

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



followers = db.Table('followers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.uid')),
    db.Column('follows_id', db.Integer, db.ForeignKey('user.uid'))
)


likes = db.Table('likes',
    db.Column('post_id', db.Integer, db.ForeignKey('post.pid')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.uid'))
)



class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)  

    follows = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.user_id == uid),
        secondaryjoin=(followers.c.follows_id == uid),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')



    def post_count(self):
        return len(self.posts)

    def get_id(self):
        return self.uid


    def is_following(self, user):
        l = self.follows.filter(followers.c.follows_id == user.uid).count()
        return l > 0


    def follow(self, user):
        if self.uid != user.uid:
            if not self.is_following(user):
                self.follows.append(user)


    def unfollow(self, user):
        if self.is_following(user):
            self.follows.remove(user)


    def get_followed_posts(self):
        fw_users = [user.uid for user in self.follows.all()]
        fw_users.append(self.uid)       # to include my own posts
        # print(fw_users)
        fw_posts = Post.query.order_by(Post.date_posted.desc()).filter(Post.user_id.in_(fw_users)).all()
        return fw_posts 


    def __repr__(self):
        return f"User('{self.username}', '{self.password}', '{self.image_file}')"



class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    media = db.Column(db.String(20), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)

    liked = db.relationship("User", secondary=likes)
    comments = db.relationship('Comment', backref='post', lazy=True)


    def get_likes_count(self):
        return len(self.liked)


    def user_liked(self, user):
        return user in self.liked


    def like_post(self, user):
        if user not in self.liked:
            self.liked.append(user)
        else:
            self.unlike_post(user)

    def unlike_post(self, user):
        self.liked.remove(user)


    def comments_count(self):
        return len(self.comments)


    def get_comments(self, limit=0):
        if limit > 0:
            return self.comments[-limit:] 


    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"


class Comment(db.Model):
    cid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.pid'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Comment({self.post_id}, {self.user_id}, '{self.content}', '{self.date_posted}')"