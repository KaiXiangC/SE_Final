from flask import Flask, render_template, redirect, url_for, request
import mysql.connector

app = Flask(__name__)

# 資料庫連線設定
db_config = {
    'host': 'your_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

@app.route('/review_comment/<int:issue_id>', methods=['GET'])
def review_comment(issue_id):
    current_index = int(request.args.get('index', 0))
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        # 抓取 Issue 表中對應的標題
        cursor.execute("SELECT title FROM Issue WHERE issueID = %s", (issue_id,))
        issue = cursor.fetchone()
        
        # 抓取 Comment 表中 review 為 false 且 issueID 匹配的資料
        cursor.execute("SELECT * FROM Comment WHERE issueID = %s AND review = false", (issue_id,))
        comments = cursor.fetchall()

        # 獲取對應的評論資料和用戶名
        if comments and 0 <= current_index < len(comments):
            comment = comments[current_index]
            cursor.execute("SELECT name FROM User WHERE userID = %s", (comment['userID'],))
            user = cursor.fetchone()
        else:
            comment = None
            user = None
    except Exception as e:
        print(f"資料庫錯誤: {e}")
        issue = None
        comments = []
        comment = None
        user = None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

    return render_template(
        'review_comment.html',
        issue=issue,
        comments=comments,
        comment=comment,
        user=user,
        current_index=current_index,
        total_comments=len(comments),
        issue_id=issue_id
    )

@app.route('/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Comment WHERE commentID = %s", (comment_id,))
        connection.commit()
    except Exception as e:
        print(f"刪除留言失敗: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return redirect(url_for('review_comment', issue_id=request.form['issue_id']))

@app.route('/approve_comment/<int:comment_id>', methods=['POST'])
def approve_comment(comment_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("UPDATE Comment SET review = true WHERE commentID = %s", (comment_id,))
        connection.commit()
    except Exception as e:
        print(f"審核留言失敗: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    return redirect(url_for('review_comment', issue_id=request.form['issue_id']))

if __name__ == '__main__':
    app.run(debug=True)
