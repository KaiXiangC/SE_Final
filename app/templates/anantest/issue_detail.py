from flask import Flask, render_template, request, redirect, url_for, flash, abort
from datetime import datetime
import os
import sqlite3

# 初始化 Flask 應用
app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'user.db'
UPLOAD_FOLDER = 'static/img'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_db():
    """連接到 SQLite 資料庫"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return "首頁"

@app.route('/issue/<int:issueID>')
def issue_detail(issueID):
    conn = get_db()

    # 獲取議題詳情
    issue = conn.execute('SELECT * FROM Issue WHERE issueID = ?', (issueID,)).fetchone()
    if not issue:
        abort(404)

    # 動態計算狀態
    current_time = datetime.now()
    if not issue['status']:
        status = "審核中"
        status_class = "reviewing"
    elif current_time > datetime.strptime(issue['deadline'], '%Y-%m-%d %H:%M:%S'):
        status = "已截止"
        status_class = "closed"
    else:
        vote_count = conn.execute('SELECT COUNT(*) FROM Vote WHERE issueID = ?', (issueID,)).fetchone()[0]
        if vote_count > 500:
            status = "已通過"
            status_class = "passed"
        else:
            status = "投票中"
            status_class = "voting"

    # 提議者
    proposer = conn.execute('SELECT name FROM User WHERE userID = ?', (issue['userID'],)).fetchone()[0]

    # 投票狀態
    user_id = 1  # 假設當前用戶
    has_voted = conn.execute('SELECT * FROM Vote WHERE issueID = ? AND userID = ?', (issueID, user_id)).fetchone()

    # 收藏狀態
    has_favorited = conn.execute('SELECT * FROM Favorite WHERE issueID = ? AND userID = ?', (issueID, user_id)).fetchone()

    # 留言
    comments = conn.execute('''
        SELECT c.content, c.commentTime, u.name AS username 
        FROM Comment c 
        JOIN User u ON c.userID = u.userID 
        WHERE c.issueID = ? 
        ORDER BY c.commentTime DESC
    ''', (issueID,)).fetchall()

    conn.close()

    return render_template(
        'issueDetail.html',
        issue=dict(issue, status=status, status_class=status_class, proposer=proposer),
        vote_count=conn.execute('SELECT COUNT(*) FROM Vote WHERE issueID = ?', (issueID,)).fetchone()[0],
        has_voted=bool(has_voted),
        has_favorited=bool(has_favorited),
        comments=comments
    )

@app.route('/vote/<int:issueID>', methods=['POST'])
def vote(issueID):
    user_id = 1  # 假設當前用戶
    conn = get_db()

    # 添加投票記錄
    conn.execute(
        'INSERT INTO Vote (voteID, userID, issueID, voteTime) VALUES (?, ?, ?, ?)',
        (f'vote_{datetime.now().timestamp()}', user_id, issueID, datetime.now())
    )
    conn.commit()
    conn.close()

    flash("投票成功！")
    return redirect(url_for('issue_detail', issueID=issueID))

@app.route('/cancel_vote/<int:issueID>', methods=['POST'])
def cancel_vote(issueID):
    user_id = 1
    conn = get_db()

    # 刪除投票記錄
    conn.execute(
        'DELETE FROM Vote WHERE userID = ? AND issueID = ?',
        (user_id, issueID)
    )
    conn.commit()
    conn.close()

    flash("已取消投票！")
    return redirect(url_for('issue_detail', issueID=issueID))

@app.route('/favorite/<int:issueID>', methods=['POST'])
def favorite(issueID):
    user_id = 1
    conn = get_db()

    # 添加收藏記錄
    conn.execute(
        'INSERT INTO Favorite (favoriteID, userID, issueID, favoriteTime) VALUES (?, ?, ?, ?)',
        (f'favorite_{datetime.now().timestamp()}', user_id, issueID, datetime.now())
    )
    conn.commit()
    conn.close()

    flash("收藏成功！")
    return redirect(url_for('issue_detail', issueID=issueID))

@app.route('/cancel_favorite/<int:issueID>', methods=['POST'])
def cancel_favorite(issueID):
    user_id = 1
    conn = get_db()

    # 刪除收藏記錄
    conn.execute(
        'DELETE FROM Favorite WHERE userID = ? AND issueID = ?',
        (user_id, issueID)
    )
    conn.commit()
    conn.close()

    flash("已取消收藏！")
    return redirect(url_for('issue_detail', issueID=issueID))

@app.route('/add_comment/<int:issueID>', methods=['POST'])
def add_comment(issueID):
    user_id = 1
    content = request.form.get('comment')
    if not content:
        flash("留言內容不能為空！")
        return redirect(url_for('issue_detail', issueID=issueID))

    conn = get_db()
    conn.execute(
        'INSERT INTO Comment (commentID, userID, issueID, commentTime, content) VALUES (?, ?, ?, ?, ?)',
        (f'comment_{datetime.now().timestamp()}', user_id, issueID, datetime.now(), content)
    )
    conn.commit()
    conn.close()

    flash("留言已成功添加！")
    return redirect(url_for('issue_detail', issueID=issueID))

if __name__ == '__main__':
    app.run(debug=True)
