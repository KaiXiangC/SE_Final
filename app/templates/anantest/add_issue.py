from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE = 'user.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/add_issue', methods=['GET'])
def add_issue():
    conn = get_db()
    categories = conn.execute('SELECT * FROM Category').fetchall()
    conn.close()
    return render_template('add_issue.html', categories=categories)

@app.route('/process_issue', methods=['POST'])
def process_issue():
    title = request.form.get('title')
    description = request.form.get('description')
    category_id = request.form.get('category')
    attachment = request.files.get('attachment')
    action = request.form.get('action')  # 新增議題或暫存議題

    if not title or not description or not category_id:
        flash("議題標題、內容描述及類別為必填項！")
        return redirect(url_for('add_issue'))

    if attachment:
        attachment_filename = attachment.filename
        attachment.save(os.path.join('uploads', attachment_filename))
    else:
        attachment_filename = None

    conn = get_db()

    if action == 'add':
        # 跳轉到 finish_issue.html
        return render_template(
            'finish_issue.html',
            title=title,
            description=description,
            category=category_id,
            attachment=attachment_filename,
        )
    elif action == 'save':
        # 將資料存入 Draft 表
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        draft_count = conn.execute('SELECT COUNT(*) FROM Draft').fetchone()[0]
        draft_id = f'draft_{draft_count + 1}'
        conn.execute(
            '''
            INSERT INTO Draft (draftID, description, categoryID, publishTime)
            VALUES (?, ?, ?, ?)
            ''',
            (draft_id, description, category_id, current_time),
        )
        conn.commit()
        conn.close()
        flash("議題已暫存！")
        return redirect(url_for('add_issue'))
    else:
        return redirect(url_for('index'))

@app.route('/')
def index():
    return "首頁"
