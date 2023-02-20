from flask import Blueprint, render_template, url_for, redirect, request, flash
from models import User, Article, Comments
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import db
from flask_login import login_user, login_required, logout_user, current_user

# Setsup the blueprint for the app
auth = Blueprint("auth", __name__)

@auth.route("/login.html", methods= ["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(first_name = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged In!", category = "success",)
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.",category="error")
        else:
            flash("Email does not exist.",category="error")

    return render_template("login.html", user = current_user)

@auth.route("/logout.html")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@auth.route("/signup", methods= ["GET", "POST"])
def signup():
    if request.method == "POST":
        firstName = request.form.get("username")
        password = request.form.get("password")
        print(password)

        user = User.query.filter_by(first_name=firstName).first()
        if user:
            flash("Email already exits", category="error")
        else:
            new_user = User(first_name = firstName,password= generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account Created!", category="success")
            return redirect(url_for("views.home"))

    return render_template("login.html", user = current_user)


