# app/routes/__init__.py

from flask import Blueprint

routes_bp = Blueprint('routes', __name__)

# 匯入所有子模組中的路由，以確保它們被註冊
from . import routes
