from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# 資料庫連線設定
db_config = {
    'host': 'your_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

@app.route('/review_issue/<int:issue_id>', methods=['GET', 'POST'])
def review_issue(issue_id):
    if request.method == 'POST':
        # 獲取表單數據
        title = request.form.get('title')
        description = request.form.get('description')
        category_name = request.form.get('category')
        
        # 更新資料庫
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            
            # 找到對應 categoryID
            cursor.execute("SELECT categoryID FROM Category WHERE name = %s", (category_name,))
            category = cursor.fetchone()
            if category:
                category_id = category[0]
                
                # 更新 Issue 資料
                cursor.execute(
                    "UPDATE Issue SET title = %s, description = %s, categoryID = %s WHERE issueID = %s",
                    (title, description, category_id, issue_id)
                )
                connection.commit()
                return jsonify({'status': 'success', 'message': '已完成儲存'})
        except Exception as e:
            print(f"更新資料失敗: {e}")
            return jsonify({'status': 'error', 'message': '儲存失敗'})
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        # 獲取 Issue 和 Category 資料
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor(dictionary=True)
            
            # 獲取議題資料
            cursor.execute("SELECT * FROM Issue WHERE issueID = %s", (issue_id,))
            issue = cursor.fetchone()
            
            # 獲取所有類別
            cursor.execute("SELECT * FROM Category")
            categories = cursor.fetchall()
        except Exception as e:
            print(f"資料庫錯誤: {e}")
            issue = None
            categories = []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
        
        return render_template('review_issue.html', issue=issue, categories=categories)

@app.route('/delete_issue/<int:issue_id>', methods=['POST'])
def delete_issue(issue_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        
        # 刪除 Issue
        cursor.execute("DELETE FROM Issue WHERE issueID = %s", (issue_id,))
        connection.commit()
    except Exception as e:
        print(f"刪除議題失敗: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
    
    return redirect(url_for('propose_manage'))  # 假設 propose_manage.html 的路由名稱是 propose_manage

if __name__ == '__main__':
    app.run(debug=True)
