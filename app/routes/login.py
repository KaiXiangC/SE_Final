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

    uncategorized_category_id = Category.get_uncategorized_category_id()

    issues_query = Issue.query.filter_by(status=True, is_review=True)
    if uncategorized_category_id:
        issues_query = issues_query.filter(Issue.categoryID != uncategorized_category_id)
    
    issues = issues_query.all()

    for issue in issues:
        issue.votes_count = len(Issue.get_votes(issue.issueID))
        issue.comments_count = len(Issue.get_comments(issue.issueID))
        issue.favorites_count = len(Issue.get_favorites(issue.issueID))

    categories = Category.get_all_categories()


    user = {
        "userID": current_user.userID,
        "name": current_user.name,
        "email": current_user.email,
    }
    return render_template(
        'index.html',
        notifications=notifications,
        issues=issues,
        categories=categories,
        admin_notifications=admin_notifications,
        user=user  # 添加用户数据
    )


@login_bp.route('/search_issues')
def search_issues():
    # 從查詢參數中獲取關鍵字
    keyword = request.args.get('keyword', '').strip()
    if not keyword:
        return jsonify({
            "status": "error",
            "message": "請提供搜尋關鍵字！"
        }), 400

    try:
        # 取得「無類別」的 categoryID
        uncategorized_category_id = Category.get_uncategorized_category_id()

        # 搜尋標題包含關鍵字且排除「無類別」的議題
        query = Issue.query.filter(
            Issue.title.like(f"%{keyword}%"),
            Issue.status == 1
        )
        if uncategorized_category_id:
            query = query.filter(Issue.categoryID != uncategorized_category_id)

        issues = query.all()
        # 如果沒找到議題
        if not issues:
            return jsonify({
                "status": "success",
                "issues": []
            })

        # 構建 JSON 響應
        result = []
        for issue in issues:
            result.append({
                "issueID": issue.issueID,
                "category": {"name": issue.category.name},
                "title": issue.title,
                "description": issue.description,
                "votes_count": len(issue.votes),
                "comments_count": len(issue.comments),
                "favorites_count": len(issue.favorites),
                "publishTime": issue.publishTime.strftime('%Y-%m-%d') if issue.publishTime else None,
                "deadline": issue.deadline.strftime('%Y-%m-%d') if issue.deadline else None,
                "status": "已通過" if issue.status else "未通過"
            })

        return jsonify({
            "status": "success",
            "issues": result
        })

    except Exception as e:
        # 處理任何潛在的錯誤
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@login_bp.route('/filter_issues_by_category', methods=['GET'])
@login_required
def filter_issues_by_category():
    category_id = request.args.get('category_id', type=int)
    if category_id is None:
        return jsonify({"status": "error", "message": "No category_id provided"}), 400

    # 使用 Category 取得該類別下的所有議題
    issues = Issue.query.filter_by(categoryID=category_id, status=True, is_review=True).all()

    # 將議題轉成可序列化的資料(JSON)
    issues_data = [{
        "issueID": i.issueID,
        "title": i.title,
        "category": {"name": i.category.name},
        "description": i.description,
        "votes_count": len(i.votes),
        "comments_count": len(i.comments),
        "favorites_count": len(i.favorites),    
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


@login_bp.route('/login/<int:user_id>/change_password', methods=['POST'])
@login_required
def change_password(user_id):
    """修改密碼"""
    if current_user.userID != user_id:
        return jsonify({'status': 'error', 'message': '您無權修改此使用者的密碼'}), 403

    user = User.query.get_or_404(user_id)
    old_password = request.form['old-password']
    new_password = request.form['new-password']
    confirm_password = request.form['confirm-password']

    # 檢查舊密碼是否正確
    if not check_password_hash(user.password, old_password):
        return jsonify({'status': 'error', 'message': '舊密碼不正確'}), 400

    # 1. 檢查新密碼是否與舊密碼相同
    if old_password == new_password:
        return jsonify({'status': 'error', 'message': '新密碼不能與舊密碼相同'}), 400

    # 檢查新密碼與確認密碼是否一致
    if new_password != confirm_password:
        return jsonify({'status': 'error', 'message': '新密碼與確認密碼不一致'}), 400

    # 更新密碼
    user.password = generate_password_hash(new_password)
    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': '密碼已更新'})
    except Exception:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': '密碼更新失敗'}), 500

@login_bp.route('/login/<int:user_id>/update_profile', methods=['POST'])
@login_required
def update_profile(user_id):
    """更新使用者資料"""
    if current_user.userID != user_id:
        return jsonify({'status': 'error', 'message': '您無權修改此使用者的資料'}), 403

    user = User.query.get_or_404(user_id)
    user.name = request.form['name']
    new_email = request.form['email']

    # 檢查電子郵件是否已經存在
    if User.query.filter_by(email=new_email).first():
        return jsonify({'status': 'error', 'message': '該電子郵件已經被使用'}), 400

    user.email = new_email

    try:
        db.session.commit()
        return jsonify({'status': 'success', 'message': '資料已更新'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': '資料更新失敗'}), 500
