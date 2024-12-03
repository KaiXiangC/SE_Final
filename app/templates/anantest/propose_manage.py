from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# 資料庫連線設定
db_config = {
    'host': 'your_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

@app.route('/')
def issue_list():
    try:
        # 連接資料庫
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # 抓取 Issue 表的資料
        query = "SELECT issueID, title FROM Issue"
        cursor.execute(query)
        issues = cursor.fetchall()
    except Exception as e:
        issues = []
        print(f"資料庫連接錯誤: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    # 傳遞資料到前端
    return render_template('issues.html', issues=issues)

@app.route('/review_comment/<int:issue_id>')
def review_comment(issue_id):
    return render_template('review_comment.html', issue_id=issue_id)

@app.route('/review_issue/<int:issue_id>')
def review_issue(issue_id):
    return render_template('review_issue.html', issue_id=issue_id)

if __name__ == '__main__':
    app.run(debug=True)
