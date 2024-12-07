from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from datetime import datetime
from app.models.issue import Issue
from app.models.user import User
from app.models.comment import Comment
from app.models.vote import Vote
from flask import jsonify
from .. import db

issue_bp = Blueprint('issue', __name__)

@issue_bp.route('/<int:issueID>')
def issue_detail(issueID):
    # 查詢議題
    issue = Issue.query.get_or_404(issueID)

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


@issue_bp.route('/<int:issueID>/vote', methods=['POST'])
@login_required
def vote(issueID):
    # 確認用戶是否已經投票
    existing_vote = Vote.query.filter_by(userID=current_user.userID, issueID=issueID).first()
    if existing_vote:
        return jsonify({'status': 'error', 'message': '你已經投過票了！'})


    # 創建新的投票記錄
    new_vote = Vote(
        userID=current_user.userID,
        issueID=issueID,
        voteOption='1',
        voteTime=datetime.now()
    )

    db.session.add(new_vote)
    db.session.commit()

    return jsonify({'status': 'success', 'message': '投票成功！'})

@issue_bp.route('/<int:issueID>/cancel_vote', methods=['POST'])
@login_required
def cancel_vote(issueID):
    # 查詢用戶是否已經投票
    existing_vote = Vote.query.filter_by(userID=current_user.userID, issueID=issueID).first()
    if not existing_vote:
        return jsonify({'status': 'error', 'message': '你還沒有投票！'})

    # 刪除投票
    db.session.delete(existing_vote)
    db.session.commit()

    return jsonify({'status': 'success', 'message': '投票已取消！'})


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