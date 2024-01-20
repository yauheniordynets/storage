# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_vue import Vue

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    Vue(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://iamjalgp:3LKSsKUu2in0JRB00flj5RsR0etCw2Ks@snuffleupagus.db.elephantsql.com/iamjalgp'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # Import your models and routes here
    from . import models

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
