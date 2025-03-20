from flask import Flask, url_for, redirect, session
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

from apps.config import config

csrf = CSRFProtect()
db = SQLAlchemy()

login_manager = LoginManager()

def create_app(config_key):
    app = Flask(__name__)
    
    app.config.from_object(config[config_key])

    csrf.init_app(app)
    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)

    @app.route("/")
    def index():
        if "user_id" in session:
            return redirect(url_for("book.index", userId=session["user_id"]))
        else:
            return redirect(url_for("auth.login"))        

    from apps.auth import view as auth_views
    from apps.book import view as book_views
    app.register_blueprint(auth_views.auth, url_prefix="/auth")
    app.register_blueprint(book_views.book, url_prefix="/book")

    return app