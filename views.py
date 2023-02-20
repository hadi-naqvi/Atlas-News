"""
This file contains all the routes for the website
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from __init__ import db
from models import User, Article, Comments
from news import search, getCountryNews
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
import json
# from flask_security import Security, SQLAlchemyUserDatastore, \
#     UserMixin, RoleMixin, login_required

# Setsup the blueprint for the app
views = Blueprint("views", __name__)

@views.route("/")
def home():
    
    return render_template("index.html", user = current_user) 


@views.route("/about.html")
def about():
    return render_template("about.html", user = current_user)

@views.route('/likearticle/<article_id>', methods=['GET'])
def like_article(article_id):
    if request.method == 'GET':
        article_liked = Article.query.filter_by(id=article_id).first()
        article_liked.likes += 1
        db.session.commit()
        return jsonify([{"done":0}])

@views.route('/dislikearticle/<article_id>', methods=['GET'])
def dislike_article(article_id):
    if request.method == 'GET':
        article_disliked = Article.query.filter_by(id=article_id).first()
        article_disliked.likes -= 1
        db.session.commit()
        return jsonify("done")

@views.route('/likecomment', methods=['POST'])
def like_comment():
    if request.method == 'POST':
        comment_id = request.form.get('comment_id')
        # have it so that clicking on a comment's like button sends the comment's id?
        comment_liked = Comments.query.filter_by(id=comment_id).first()
        comment_liked.likes += 1
        db.session.commit()

@views.route('/dislikecommment', methods=['POST'])
def dislike_comment():
    if request.method == 'POST':
        comment_id = request.form.get('comment_id')
        # have it so that clicking on a comment's dislike button sends the article's id?
        comment_disliked = Comments.query.filter_by(id=comment_id).first()
        comment_disliked.likes -= 1
        db.session.commit()

@views.route('/postcomment', methods=['POST'])
def post_comment():
    if request.method == 'POST':
        user_id = get_user_id()
        user = User.query.filter_by(id = user_id).first()
        comment = request.form.get("post")
        article_id = request.form.get("article-id")
        new_comment = Comments(user_id=user_id, article_id=article_id, comment=comment)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify([{"comment":comment}])

@views.route('/getcomments/<article_id>', methods=['GET'])
def get_comments(article_id):
    if request.method == 'GET':
        article = Article.query.filter_by(id = article_id).first()
        comments = article.comments
        comments_2 = []
        for comment in comments:
            comments_2.append({"comment": comment.comment, "date": comment.date, "user_id": comment.user_id})
        print(comments_2)
        return jsonify(comments_2)
        
def archive_articles_top(articles):  # country-specific
    for article in articles: 
        new_article = Article(title = article["title"], url =article["url"], image_url= article["urlToImage"], source= article["source"]["name"], likes= 0, date = article["publishedAt"], country = article["country"])
        existing_article = Article.query.filter_by(url=new_article.url).first()
        if not existing_article:
            db.session.add(new_article)
            db.session.commit()
            
def archive_articles(articles):  # from search
    for article in articles: 
        new_article = Article(title = article["title"], url =article["url"],image_url= article["urlToImage"], source= article["source"]["name"],likes= 0, date = article["publishedAt"])
        existing_article = Article.query.filter_by(url = new_article.url).first()
        if not existing_article:
            db.session.add(new_article)
            db.session.commit()

@views.route("/getarticle/<article_id>")
def get_article(article_id):
    existing_article = Article.query.filter_by(id = article_id).first()
    return jsonify([{"title": existing_article.title , "url": existing_article.url, "image_url":existing_article.image_url, "source": existing_article.source, "likes": existing_article.likes, "date": existing_article.date}])


@views.route("/country/<country>", methods = ["GET"])
def get_country_articles(country):
    articles = getCountryNews(country)
    archive_articles_top(articles["articles"])

    for article in articles["articles"]:
        existing_article = Article.query.filter_by(url= article["url"]).first()
        article["id"] = existing_article.id
    return jsonify(articles["articles"])

@views.route("/search/<query>", methods = ["GET"])
def search_bar(query):
    articles = search(query=query)
    archive_articles(articles["articles"])
    
    for article in articles["articles"]:
        existing_article = Article.query.filter_by(url= article["url"]).first()
        article["id"] = existing_article.id
    return jsonify(articles["articles"])

def get_user_id():
    return current_user.id

@views.route("/getuser/<user_id>", methods = ["GET"])
def getUser(user_id):
    user = User.query.filter_by(id = user_id).first()
    print(user)
    return jsonify([{"first_name": user.first_name}])

    








