from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import logging

# 設置日誌記錄
logging.basicConfig(level=logging.DEBUG)

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.home'

    @login_manager.user_loader
    def load_user(user_id):
        from .models.user import User
        return User.query.get(int(user_id))
    
    # 測試組用Blueprint
    from .routes.routes import routes_bp
    from .routes.issue import issue_bp
    from .routes.hist import hist_bp
    from .routes.notification import noti_bp
    from .routes.main import main_bp
    from .routes.member import member_bp
    from .routes.login import login_bp
    from .routes.register import register_bp
    from .routes.admin import admin_bp

    app.register_blueprint(routes_bp, url_prefix='/test')  # 您可以根據需要更改 url_prefix
    app.register_blueprint(issue_bp, url_prefix='/issue')
    app.register_blueprint(hist_bp, url_prefix='/hist')
    app.register_blueprint(noti_bp, url_prefix='/notification')
    app.register_blueprint(main_bp)
    app.register_blueprint(member_bp, url_prefix='/member')
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(admin_bp)

    return app

'''
    from .routes.main import configure_routes
    configure_routes(app)
'''
    