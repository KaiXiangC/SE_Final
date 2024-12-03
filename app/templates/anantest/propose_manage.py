from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用於加密 flash 消息

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
        query = "SELECT issueID, title, review FROM Issue"
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
    return render_template('propose_manage.html', issues=issues)

@app.route('/approve_issue/<int:issue_id>', methods=['POST'])
def approve_issue(issue_id):
    try:
        # 連接資料庫
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # 更新 Issue 表的 review 欄位為 true
        query = "UPDATE Issue SET review = true WHERE issueID = %s"
        cursor.execute(query, (issue_id,))
        connection.commit()
        
        # 添加成功通知
        flash('審核成功！', 'success')
    except Exception as e:
        print(f"審核失敗: {e}")
        flash('審核失敗！請稍後再試。', 'error')
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    # 審核完成後重定向回主頁
    return redirect(url_for('issue_list'))

if __name__ == '__main__':
    app.run(debug=True)
