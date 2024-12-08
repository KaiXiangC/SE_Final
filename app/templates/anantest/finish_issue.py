from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
import os
import sqlite3
import uuid

# 初始化 Flask
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 配置圖片存放路徑
UPLOAD_FOLDER = 'static/img'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 數據庫配置
DATABASE = 'user.db'

def get_db():
    """連接到 SQLite 資料庫"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# 首頁
@app.route('/')
def index():
    return "首頁"

# 新增議題頁面
@app.route('/add_issue', methods=['GET'])
def add_issue():
    conn = get_db()
    categories = conn.execute('SELECT * FROM Category').fetchall()
    conn.close()
    return render_template('add_issue.html', categories=categories)

# 提交議題（預覽頁面）
@app.route('/preview_issue', methods=['POST'])
def preview_issue():
    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category')
    attachment = request.files.get('attachment')
    user_id = 1  # 假設當前用戶 ID

    # 必填檢查
    if not title or not description or not category_id:
        flash("議題標題、內容描述及類別為必填項！")
        return redirect(url_for('add_issue'))

    # 保存圖片
    attachment_filename = None
    if attachment:
        attachment_filename = f"{uuid.uuid4().hex}_{attachment.filename}"
        attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], attachment_filename))

    conn = get_db()
    categories = conn.execute('SELECT * FROM Category').fetchall()
    proposer_name = conn.execute('SELECT name FROM User WHERE userID = ?', (user_id,)).fetchone()[0]
    conn.close()

    return render_template(
        'finish_issue.html',
        title=title,
        description=description,
        selected_category=category_id,
        attachment=attachment_filename,
        proposer_name=proposer_name,
        categories=categories
    )

# 最終提交議題
@app.route('/finalize_issue', methods=['POST'])
def finalize_issue():
    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category')
    new_attachment = request.files.get('attachment')  # 新上傳的圖片
    old_attachment = request.form.get('old_attachment')  # 舊圖片檔案名
    user_id = 1  # 假設當前用戶 ID

    # 必填檢查
    if not title or not description or not category_id:
        flash("所有欄位必須填寫！")
        return redirect(url_for('add_issue'))

    # 處理圖片上傳與替換
    attachment_filename = old_attachment  # 默認使用舊圖片
    if new_attachment:
        # 刪除舊圖片
        if old_attachment:
            old_attachment_path = os.path.join(app.config['UPLOAD_FOLDER'], old_attachment)
            if os.path.exists(old_attachment_path):
                os.remove(old_attachment_path)

        # 保存新圖片
        attachment_filename = f"{uuid.uuid4().hex}_{new_attachment.filename}"
        new_attachment.save(os.path.join(app.config['UPLOAD_FOLDER'], attachment_filename))

    conn = get_db()
    current_time = datetime.now()
    deadline = current_time + timedelta(days=60)

    # 自動生成 issueID
    issue_count = conn.execute('SELECT COUNT(*) FROM Issue').fetchone()[0]
    issue_id = f'issue_{issue_count + 1}'

    # 插入數據到 Issue 表
    conn.execute(
        '''
        INSERT INTO Issue (issueID, userID, title, description, categoryID, publishTime, deadline, attachment)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (issue_id, user_id, title, description, category_id, current_time, deadline, attachment_filename)
    )
    conn.commit()
    conn.close()

    flash("議題已成功提交！")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
