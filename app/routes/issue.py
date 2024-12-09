import os

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime

from werkzeug.utils import secure_filename

from app.models import Vote, Category, Comment, Issue, User, Favorite
from flask import jsonify
from .. import db


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
issue_bp = Blueprint('issue', __name__)
UPLOAD_FOLDER = os.path.join('app', 'static', 'img')

@issue_bp.route('/<int:issueID>')
def issue_detail(issueID):
    # 查詢議題
    issue = Issue.query.get_or_404(issueID)
    if issue.status == 0:
        flash('該議題尚未公開，無法檢視。', 'warning')
        return redirect(url_for('index'))  # 導回首頁
    # 格式化剩餘時間
    deadline_str = None
    if issue.deadline:
        remaining = issue.deadline - datetime.now()
        days_left = remaining.days
        deadline_str = f"{days_left}天後截止" if days_left > 0 else "已截止"
    # 查詢是否已經投票
    existing_vote = Vote.query.filter_by(userID=current_user.userID, issueID=issueID).first()
    has_voted = True if existing_vote else False

    # 查詢相關評論
    comments = Comment.query.filter_by(issueID=issueID).order_by(Comment.commentTime.desc()).all()

    vote_count = Vote.query.filter_by(issueID=issueID).count()
    # 查找每條評論的 username
    comments_data = []
    for comment in comments:
        user = User.query.get(comment.userID)  # 根據 userID 查找 User
        comments_data.append({
            'username': user.name if user else 'Unknown',  # 如果找不到對應的 user，顯示 'Unknown'
            'content': comment.content,
            'time': comment.commentTime
        })

    return render_template(
        'issueDetail.html',
        issueID=issueID,
        has_voted=has_voted,
        issue={
            'title': issue.title,
            'status': issue.status,
            'deadline': deadline_str,
            'username': issue.userID,  # 假設 userID 對應名稱需要額外查詢
            'image1': issue.attachment_1,
            'image2': issue.attachment_2,
            'description': issue.description
        },
        vote_count=vote_count,
        comments=comments_data
    )


@issue_bp.route('/<int:issueID>/comment', methods=['POST'])
@login_required
def add_comment(issueID):
    # 獲取表單內容
    content = request.form.get('comment')
    if not content:
        return jsonify({'status': 'error', 'message': '評論內容不能為空'})

    # 創建新評論
    new_comment = Comment(
        userID=current_user.userID,  # 使用 current_user 的 ID
        issueID=issueID,
        content=content,
        commentTime=datetime.now(),
        is_review=False  # 默認為未審核
    )

    db.session.add(new_comment)
    db.session.commit()

    # 返回 JSON 回應
    return jsonify({'status': 'success', 'message': '評論已提交！'})


# @issue_bp.route('/<int:issueID>/vote', methods=['POST'])
# @login_required
# def vote(issueID):
#     # 確認用戶是否已經投票
#     existing_vote = Vote.query.filter_by(userID=current_user.userID, issueID=issueID).first()
#     if existing_vote:
#         return jsonify({'status': 'error', 'message': '你已經投過票了！'})
#
#
#     # 創建新的投票記錄
#     new_vote = Vote(
#         userID=current_user.userID,
#         issueID=issueID,
#         voteOption='1',
#         voteTime=datetime.now()
#     )
#
#     db.session.add(new_vote)
#     db.session.commit()
#
#     return jsonify({'status': 'success', 'message': '投票成功！'})

@issue_bp.route('/vote/<int:issueID>', methods=['POST'])
@login_required
def vote(issueID):
    issue = Issue.query.get_or_404(issueID)

    # 檢查用戶是否已經投票
    existing_vote = Vote.query.filter_by(userID=current_user.userID, issueID=issueID).first()

    if existing_vote:
        # 用戶已投票，取消投票
        db.session.delete(existing_vote)
        is_vote = False
        message = '取消投票成功！'
    else:
        # 用戶尚未投票，新增投票
        new_vote = Vote(
            userID=current_user.userID,
            issueID=issueID,
            voteTime=datetime.now()
        )
        db.session.add(new_vote)
        is_vote = True
        message = '投票成功！'

    try:
        db.session.commit()

        # 返回更新後的投票狀態和投票數量
        vote_count = Vote.query.filter_by(issueID=issueID).count()
        return jsonify({
            'status': 'success',
            'is_vote': is_vote,
            'vote_count': vote_count,
            'message': message
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@issue_bp.route('/favorite/<int:issueID>', methods=['POST'])
@login_required
def favorite(issueID):
    issue = Issue.query.get_or_404(issueID)

    # 檢查用戶是否已收藏
    existing_favorite = Favorite.query.filter_by(
        userID=current_user.userID,
        issueID=issueID
    ).first()

    if existing_favorite:
        # 如果已收藏，則取消收藏
        db.session.delete(existing_favorite)
        is_favorited = False
        message = '取消收藏成功！'
    else:
        # 如果未收藏，則添加收藏
        new_favorite = Favorite(
            userID=current_user.userID,
            issueID=issueID,
            favoriteTime=datetime.now()
        )
        db.session.add(new_favorite)
        is_favorited = True
        message = '收藏成功！'

    try:
        db.session.commit()
        return jsonify({
            'status': 'success',
            'is_favorited': is_favorited,
            'favorite_count': Favorite.query.filter_by(issueID=issueID).count(),
            'message': message
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# @issue_bp.route('/<int:issueID>/cancel_vote', methods=['POST'])
# @login_required
# def cancel_vote(issueID):
#     # 查詢用戶是否已經投票
#     existing_vote = Vote.query.filter_by(userID=current_user.userID, issueID=issueID).first()
#     if not existing_vote:
#         return jsonify({'status': 'error', 'message': '你還沒有投票！'})
#
#     # 刪除投票
#     db.session.delete(existing_vote)
#     db.session.commit()
#
#     return jsonify({'status': 'success', 'message': '投票已取消！'})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@issue_bp.route('/process_issue', methods=['GET', 'POST'])
@issue_bp.route('/process_issue/<int:issueID>', methods=['GET', 'POST'])
@login_required
def new_issue(issueID=None):
    if request.method == 'GET':
        categories = Category.query.all()  # 查詢所有類別
        if issueID:
            issue = Issue.query.get_or_404(issueID)
            if issue.userID != current_user.userID or issue.status != 0:
                flash('這個議題無法編輯', 'warning')
                print("aaa")
                return redirect(url_for('index'))  # 如果不是該用戶的暫存議題，則跳轉
            return render_template('add_issue.html', categories=categories, issue=issue)
        else:
            return render_template('add_issue.html', categories=categories)

    # POST 請求處理表單提交
    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category')
    action_1 = request.form.get('action_1')  # 會收到 "add" 或 "save"
    attachment = request.files.get('attachment')
    attachment_2 = request.files.get('attachment_2')

    if not title or not description or not category_id:
        flash('所有必填欄位都必須填寫！', 'warning')
        return redirect(url_for('issue.process_issue', issueID=issueID))

    def save_attachment(attachment):
        if attachment and allowed_file(attachment.filename):
            filename = secure_filename(attachment.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            attachment.save(file_path)
            return filename
        return None

    attachment_filename_1 = save_attachment(attachment)
    attachment_filename_2 = save_attachment(attachment_2)

    if action_1 == 'save':
        # 創建議題
        if issueID:
            issue = Issue.query.get_or_404(issueID)
            # 更新議題
            issue.title = title
            issue.description = description
            issue.categoryID = category_id
            issue.attachment_1 = attachment_filename_1
            issue.attachment_2 = attachment_filename_2
            issue.status = 0  # 確保為暫存狀態
            db.session.commit()
            flash('議題已保存', 'info')
            return redirect(url_for('issue.issue_detail', issueID=issue.issueID))
        else:
            # 創建新議題
            new_issue = Issue(
                title=title,
                description=description,
                categoryID=category_id,
                userID=current_user.userID,
                attachment_1=attachment_filename_1,
                attachment_2=attachment_filename_2,
                publishTime=datetime.now(),
                status=0  # 暫存狀態
            )
            db.session.add(new_issue)
            db.session.commit()
            flash('議題已暫存', 'info')
            return redirect(url_for('issue.issue_detail', issueID=new_issue.issueID))

    categories = Category.query.all()  # 假設有 Category 模型
    return render_template(
        'finish_issue.html',
        title=title,
        description=description,
        attachment_1=attachment_filename_1,
        attachment_2=attachment_filename_2,
        categories=categories,
        selected_category=int(category_id),
        proposer_name=current_user.name
    )





@issue_bp.route('/finalize_issue', methods=['GET', 'POST'])
def finalize_issue():

    if request.method == 'POST':
        action = request.form.get('action')
        title = request.form.get('title')  # 從表單中獲取
        description = request.form.get('description')  # 從表單中獲取
        attachment_1 = request.form.get('attachment_1')
        attachment_2 = request.form.get('attachment_2')
        category_id = request.form.get('category')

        if not title or not description or not category_id:
            flash('請確保所有欄位都已填寫！', 'danger')
            return redirect(url_for('issue.finalize_issue'))
        # 儲存最終資料到資料庫
        if action == 'add':
            # 儲存議題
            new_issue = Issue(
                title=title,
                description=description,
                categoryID=category_id,
                userID=current_user.userID,
                attachment_1=attachment_1,
                attachment_2=attachment_2,
                publishTime=datetime.now(),
                status=1  # 假設為草稿狀態
            )

            db.session.add(new_issue)
            db.session.commit()
            flash('議題成功新增!', 'success')
            return redirect(url_for('issue.issue_detail', issueID=new_issue.issueID))



        return redirect(url_for('index'))  # 取消或其他操作

    categories = Category.query.all()
    return render_template(
        'finish_issue.html',
        title=request.args.get('title'),  # 可以從 URL 參數中獲取
        description=request.args.get('description'),  # 可以從 URL 參數中獲取
        attachment_1=request.args.get('attachment_1'),
        attachment_2=request.args.get('attachment_2'),
        categories=categories,
        selected_category=request.args.get('category_id')
    )

# @issue_bp.route('/issue/<int:issueID>/comment', methods=['POST'])
# @login_required
# def add_comment(issueID):
#     # 獲取表單內容
#     content = request.form.get('comment')
#     if not content:
#         flash("評論內容不能為空", "warning")
#         return redirect(url_for('issue.issue_detail', issueID=issueID))
#
#     # 創建新評論
#     new_comment = Comment(
#         userID=current_user.userID,  # 使用 current_user 的 ID
#         issueID=issueID,
#         content=content,
#         commentTime=datetime.now(),
#         is_review=False  # 默認為未審核
#     )
#
#     db.session.add(new_comment)
#     db.session.commit()
#     flash("評論已提交！", "success")
#
#     return redirect(url_for('issue.issue_detail', issueID=issueID))
# @issue_bp.route('/issue/<int:issueID>/vote', methods=['POST'])
# @login_required
# def vote(issueID):
#     # 確認用戶是否已經投票
#     existing_vote = Vote.query.filter_by(userID=current_user.userID, issueID=issueID).first()
#     if existing_vote:
#         flash("你已經投過票了！", "warning")
#         return redirect(url_for('issue.issue_detail', issueID=issueID))
#
#     # 獲取用戶的選擇
#     # vote_option = request.form.get('vote_option')
#     # if not vote_option:
#     #     flash("請選擇一個投票選項！", "warning")
#     #     return redirect(url_for('issue.issue_detail', issueID=issueID))
#
#     # 創建新的投票記錄
#     new_vote = Vote(
#         userID=current_user.userID,
#         issueID=issueID,
#         voteOption='vote_option',
#         voteTime=datetime.now()
#     )
#
#     db.session.add(new_vote)
#     db.session.commit()
#
#     flash("投票成功！", "success")
#     return redirect(url_for('issue.issue_detail', issueID=issueID))
#
#
# @issue_bp.route('/issue/<int:issueID>/cancel_vote', methods=['POST'])
# @login_required
# def cancel_vote(issueID):
#     # 查找用戶的投票記錄
#     existing_vote = Vote.query.filter_by(userID=current_user.userID, issueID=issueID).first()
#     if not existing_vote:
#         flash("你還沒有投票！", "warning")
#         return redirect(url_for('issue.issue_detail', issueID=issueID))
#
#     # 刪除用戶的投票記錄
#     db.session.delete(existing_vote)
#     db.session.commit()
#
#     flash("投票已取消！", "success")
#     return redirect(url_for('issue.issue_detail', issueID=issueID))