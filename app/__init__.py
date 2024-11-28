from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # 修改為您的資料庫 URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # 初始化 Flask-Migrate

    # 註冊模型並創建資料表
    with app.app_context():
        from .models import *
        db.create_all()

    # 註冊 Blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
