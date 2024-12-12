from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from app import db
<<<<<<< Updated upstream
from app.models import User, Notification
import os
=======
from app.models.user import User
from app.models.notification import Notification
from app.models.issue import Issue
>>>>>>> Stashed changes

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
        """登入"""
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            user = User.query.filter_by(email=email).first()

            if user and check_password_hash(user.password, password):
                if user.authenticationStatus == False:
                    flash('帳號未驗證', 'danger')
                    return render_template('login.html', error='帳號未驗證')
                else:
                        login_user(user)
                        flash('登入成功', 'success')
                        if user.is_admin:
                                return redirect(url_for('login.admin_dashboard'))
                        else:
                                return redirect(url_for('login.index', user_id=user.userID))
            else:
                flash('帳號或密碼錯誤', 'danger')
                return render_template('login.html', error='帳號或密碼錯誤')
        
        return render_template('login.html')

@login_bp.route('/index')
@login_required
def index():
<<<<<<< Updated upstream
        """首頁"""
        notifications = Notification.query.all()
        return render_template('index.html', notifications=notifications)

@login_bp.route('/api/ad')
@login_required
def api_ad():
    img_folder = os.path.join('app', 'static', 'img')
    images = [f for f in os.listdir(img_folder) if 'ad' in f and f.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return jsonify(images)
=======
    user_id = current_user.userID  # 假設 current_user 有 userID 屬性
    
    # 取得通知及所有 Issue
    notifications = Notification.get_notifications_by_user(user_id)
    issues = Issue.get_all_issues()
    print(issues)
    return render_template('index.html',
                           notifications=notifications,
                           issues=issues)
>>>>>>> Stashed changes

@login_bp.route('/logout')
@login_required
def logout():
        """登出"""
        logout_user()
        flash('您已登出', 'success')
        return redirect(url_for('login.login'))

@login_bp.route('/admin_dashboard')
@login_required
def admin_dashboard():
        """管理員儀表板"""
        return render_template('member_homepage.html')