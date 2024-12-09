from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from app.models.issue import Issue
from app.models.comment import Comment
from app.models.favorite import Favorite
from app.models.vote import Vote
from app import db

hist_bp = Blueprint('hist', __name__)

@hist_bp.route('/history', methods=['GET'])
def history():
    user_id = current_user.userID

    posted_issues = Issue.get_posted_issues_by_user(user_id)
    commented_issues = Comment.get_commented_issues_by_user(user_id)
    favorited_issues = Favorite.get_favorited_issues_by_user(user_id)
    voted_issues = Vote.get_voted_issues_by_user(user_id)
    
    # 預設顯示全部互動過的議題
    all_issues = set(posted_issues + commented_issues + favorited_issues + voted_issues)

    issues_info = []
    for issue in all_issues:
        icons = []
        if issue.userID == user_id:
            icons.append('<span style="font-size: 24px;">✍️</span>')
        if issue in commented_issues:
            icons.append('<span style="font-size: 24px;">💬</span>')
        if issue in voted_issues:
            icons.append('<span style="font-size: 24px;">🗳️</span>')
        if issue in favorited_issues:
            icons.append('<span style="color: yellow;">★</span>')

        preview_length = 50
        preview = issue.description[:preview_length] + '...' if len(issue.description) > preview_length else issue.description

        issues_info.append({
            'issueID': issue.issueID,
            'title': issue.title,
            'preview': preview,
            'icons': ' '.join(icons)
        })

    return render_template('history.html', issues=issues_info)

@hist_bp.route('/history/filter', methods=['GET'])
def history_filter():
    user_id = current_user.userID
    filter_type = request.args.get('filter', None)
    
    posted_issues = Issue.get_posted_issues_by_user(user_id)
    commented_issues = Comment.get_commented_issues_by_user(user_id)
    favorited_issues = Favorite.get_favorited_issues_by_user(user_id)
    voted_issues = Vote.get_voted_issues_by_user(user_id)

    if filter_type == 'created':
        target_issues = posted_issues
    elif filter_type == 'commented':
        target_issues = commented_issues
    elif filter_type == 'favorited':
        target_issues = favorited_issues
    elif filter_type == 'voted':
        target_issues = voted_issues
    else:
        # 無篩選條件，顯示全部
        target_issues = set(posted_issues + commented_issues + favorited_issues + voted_issues)

    issues_data = []
    for issue in target_issues:
        icons = []
        if issue.userID == user_id:
            icons.append('✍️')
        if issue in commented_issues:
            icons.append('💬')
        if issue in voted_issues:
            icons.append('🗳️')
        if issue in favorited_issues:
            icons.append('★')

        preview_length = 50
        preview = issue.description[:preview_length] + '...' if len(issue.description) > preview_length else issue.description

        issues_data.append({
            'issueID': issue.issueID,
            'title': issue.title,
            'preview': preview,
            'icons': icons
        })

    return jsonify(issues_data)
