@app.route('/issue/<int:issueID>')
def issue_detail(issueID):
    conn = get_db()

    # 獲取議題詳情
    issue = conn.execute('SELECT * FROM Issue WHERE issueID = ?', (issueID,)).fetchone()
    if not issue:
        abort(404)

    # 動態計算議題狀態
    current_time = datetime.now()
    status = "審核中" if not issue['status'] else \
             "已截止" if current_time > datetime.strptime(issue['deadline'], '%Y-%m-%d') else \
             "已通過" if conn.execute('SELECT COUNT(*) FROM Vote WHERE issueID = ?', (issueID,)).fetchone()[0] > 500 else \
             "投票中"

    # 獲取提議者
    proposer = conn.execute('SELECT name FROM User WHERE userID = ?', (issue['userID'],)).fetchone()[0]

    # 獲取投票數
    vote_count = conn.execute('SELECT COUNT(*) FROM Vote WHERE issueID = ?', (issueID,)).fetchone()[0]

    # 檢查是否已投票
    has_voted = conn.execute('SELECT * FROM Vote WHERE issueID = ? AND userID = ?', (issueID, current_user.id)).fetchone()

    # 檢查是否已收藏
    has_favorited = conn.execute('SELECT * FROM Favorite WHERE issueID = ? AND userID = ?', (issueID, current_user.id)).fetchone()

    # 獲取留言
    comments = conn.execute('SELECT c.content, c.commentTime, u.name AS username FROM Comment c JOIN User u ON c.userID = u.userID WHERE c.issueID = ?', (issueID,)).fetchall()

    conn.close()

    return render_template(
        'issueDetail.html',
        issue=dict(issue, status=status, proposer=proposer),
        vote_count=vote_count,
        has_voted=bool(has_voted),
        has_favorited=bool(has_favorited),
        comments=comments
    )
