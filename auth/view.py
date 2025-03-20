import requests

from flask import Blueprint, render_template, url_for, flash, redirect, request, session, g
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from apps.app import db
from apps.auth.forms import SignUpForm, LoginForm
from apps.auth.models import User
from apps.book.models import Board

auth = Blueprint (
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",    
)

@auth.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
        # g.board = 

@auth.route("/signup", methods=["GET", "POST"])
def create_user():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            userId = form.id.data,
            password = form.password.data,
            userName = form.username.data,
            userPhoneNumber = form.phonenumber.data,
            userEmail = form.email.data
        )

        db.session.add(user)
        db.session.commit()

        login_user(user)

        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/") :
            next_ = url_for("auth.login")
        return redirect(next_)

    return render_template("signup.html", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():        
        user = User.query.filter_by(userId=form.id.data).first()

        if user is not None and user.verify_password(form.password.data):
            login_user(user)

            session["user_id"] = user.userId

            return redirect(url_for("book.index", userId=session["user_id"]))
    
    return render_template("login.html", form=form)

@auth.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("auth.login"))