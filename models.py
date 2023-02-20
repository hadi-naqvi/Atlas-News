from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), unique=False)
    password = db.Column(db.String(150))
    comments = db.relationship("Comments")

class Article(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String())
    url = db.Column(db.String(), unique=True)
    image_url = db.Column(db.String())
    source = db.Column(db.String())
    likes = db.Column(db.Integer)
    comments = db.relationship("Comments")
    date = db.Column(db.String())
    country = db.Column(db.String())

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    article_id = db.Column(db.Integer, db.ForeignKey("article.id"))
    comment = db.Column(db.String(2000))
    date = db.Column(db.DateTime(timezone= True), default= func.now())
