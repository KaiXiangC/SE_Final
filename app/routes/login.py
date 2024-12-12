from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from app import db
from app.models.user import User
from app.models.notification import Notification
from app.models.issue import Issue
from app.models.category import Category

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
    user_id = current_user.userID

    # 使用者本身的通知
    raw_notifications = Notification.get_notifications_by_user(user_id)
    notifications = [n.to_dict() for n in raw_notifications]

    # 取得管理員的通知
    admin_raw_notifications = Notification.get_admin_notifications()
    admin_notifications = [n.to_dict() for n in admin_raw_notifications]

    # 取得議題、類別等...
    issues = Issue.get_all_issues()
    for issue in issues:
        issue.votes_count = len(Issue.get_votes(issue.issueID))
        issue.comments_count = len(Issue.get_comments(issue.issueID))
        issue.favorites_count = len(Issue.get_favorites(issue.issueID))

    categories = Category.get_all_categories()

    return render_template(
        'index.html',
        notifications=notifications,
        issues=issues,
        categories=categories,
        admin_notifications=admin_notifications
    )


@login_bp.route('/filter_issues_by_category', methods=['GET'])
@login_required
def filter_issues_by_category():
    category_id = request.args.get('category_id', type=int)
    if category_id is None:
        return jsonify({"status": "error", "message": "No category_id provided"}), 400

    # 使用 Category 取得該類別下的所有議題
    issues = Category.get_issues_by_category_id(category_id)
    # 將議題轉成可序列化的資料(JSON)
    issues_data = [{
        "issueID": i.issueID,
        "title": i.title,
        "description": i.description,
        "publishTime": i.publishTime.isoformat() if i.publishTime else None,
        "deadline": i.deadline.isoformat() if i.deadline else None,
        "is_review": i.is_review,
        "status": i.status
    } for i in issues]

    return jsonify({"status": "success", "issues": issues_data})

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