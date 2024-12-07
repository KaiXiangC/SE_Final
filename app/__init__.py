from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    # 測試組用Blueprint
    from app.routes import routes_bp
    from .routes.issue import issue_bp
    app.register_blueprint(routes_bp, url_prefix='/test')  # 您可以根據需要更改 url_prefix
    app.register_blueprint(issue_bp, url_prefix='/issue')

    from app.routes.main import configure_routes
    configure_routes(app)

    return app