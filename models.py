from extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime

#list of stories they've created and saved
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#add genre
class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    story_id = db.Column(db.Integer, db.ForeignKey("story.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    #created_at = db.Column(db.DateTime, default=datetime.now)

class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_id = db.Column(db.Integer, db.ForeignKey("story.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
