from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 初始化擴展
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # 從 config.py 加載配置

    # 初始化資料庫和遷移
    db.init_app(app)
    migrate.init_app(app, db)

    # 註冊藍圖
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
