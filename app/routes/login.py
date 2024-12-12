from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from app import db
from app.models.user import User

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
        """首頁"""
        return render_template('index.html')

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