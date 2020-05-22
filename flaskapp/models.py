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

class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(32), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    
    posts = db.relationship('Post', backref='author', lazy=True) 


    def get_id(self):
        return self.uid


    def __repr__(self):
        return f"User('{self.username}', '{self.password}', '{self.image_file}')"



class Post(db.Model):
    pid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'), nullable=False)

    def __repr__(self):
        return f"Post('{self.content}', '{self.date_posted}')"