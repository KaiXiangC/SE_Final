from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# 初始化擴展
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # 初始化 Flask 應用
    app = Flask(__name__, template_folder='templates')
    
    # 設置密鑰與加載配置
    app.config.from_object(Config)
    
    # 初始化資料庫和遷移
    db.init_app(app)
    migrate.init_app(app, db)

    # 測試組用Blueprint
    from app.routes import routes_bp
    app.register_blueprint(routes_bp, url_prefix='/test')  # 您可以根據需要更改 url_prefix

    # 引入模型以確保資料庫表正確生成
    with app.app_context():
        from app.models import Notification, User, Vote, Favorite, Issue, Comment, Category

    return app