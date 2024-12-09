from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # 修改為你的資料庫 URI
db = SQLAlchemy(app)

# 定義模型
class Issue(db.Model):
    issueID = db.Column(db.Integer, primary_key=True)
    categoryID = db.Column(db.Integer, db.ForeignKey('category.categoryID'))
    title = db.Column(db.String(255))
    publishTime = db.Column(db.DateTime)

class Comment(db.Model):
    commentID = db.Column(db.Integer, primary_key=True)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'))

class Favorite(db.Model):
    favoriteID = db.Column(db.Integer, primary_key=True)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'))

class Vote(db.Model):
    voteID = db.Column(db.Integer, primary_key=True)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'))

class Category(db.Model):
    categoryID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    keyword = request.json.get('keyword', '')
    
    # 查找與關鍵字匹配的所有問題
    if keyword:
        issues = Issue.query.filter(Issue.title.contains(keyword)).all()
    else:
        issues = Issue.query.all()  # 沒有關鍵字，返回所有資料

    results = []

    for issue in issues:
        comment_count = Comment.query.filter_by(issueID=issue.issueID).count()
        favorite_count = Favorite.query.filter_by(issueID=issue.issueID).count()
        vote_count = Vote.query.filter_by(issueID=issue.issueID).count()
        category_name = Category.query.filter_by(categoryID=issue.categoryID).first().name

        results.append({
            'title': issue.title,
            'publishTime': issue.publishTime.strftime('%Y-%m-%d'),
            'commentCount': comment_count,
            'favoriteCount': favorite_count,
            'voteCount': vote_count,
            'categoryName': category_name,
            'issueID': issue.issueID
        })

    return jsonify(results)

@app.route('/issue_detail/<int:issueID>')
def issue_detail(issueID):
    issue = Issue.query.get_or_404(issueID)
    return render_template('issue_detail.html', issue=issue)

@app.route('/announcements')
def announcements():
    conn = get_db()

    # 獲取 Notification 表中最新的 5 筆資料
    notifications = conn.execute(
        'SELECT content FROM Notification ORDER BY notificationTime DESC LIMIT 5'
    ).fetchall()

    conn.close()

    # 傳遞數據到前端
    return render_template('announcements.html', notifications=notifications)


if __name__ == '__main__':
    app.run(debug=True)
