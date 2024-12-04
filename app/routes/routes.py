# app/routes/routes.py

from . import routes_bp
from app.models.user import User


## 暫時查詢用
@routes_bp.route('/users', methods=['GET'])
def show_users():
    # 查詢所有 User 資料
    users = User.query.all()

    # 構建純文字格式的結果
    user_list = "\n".join([f"Name: {user.name}, Email: {user.email}" for user in users])
    
    return user_list  # 返回純文字