from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models.notification import Notification

noti_bp = Blueprint('notification', __name__)

@noti_bp.route('/', methods=['GET'])
@login_required
def view_notifications():
    # 支援標題搜尋
    search_title = request.args.get('q', '').strip()
    # 根據目前登入的使用者 (current_user) 和搜尋標題過濾公告
    notifications = Notification.query.filter(
        Notification.userID == current_user.userID,  # 限制公告屬於當前使用者
        Notification.title.ilike(f"%{search_title}%")  # 支援標題模糊搜尋 (大小寫不敏感)
    ).order_by(Notification.createTime.desc()).all()  # 按建立時間排序

    # 顯示公告主頁面
    return render_template('notifications.html', 
                           notifications=notifications, 
                           search_title=search_title)
    

@noti_bp.route('/create', methods=['POST'])
@login_required
def create_notification():
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        return jsonify({'status': 'error', 'message': '標題與內容不可為空'}), 400

    new_notif = Notification.create_notification(current_user.userID, title, content)
    if new_notif:
        return jsonify({
            'status': 'success', 
            'message': '公告已建立',
            'notificationID': new_notif.notificationID,
            'title': new_notif.title,
            'content': new_notif.content
        })
    else:
        return jsonify({'status': 'error', 'message': '建立公告時發生錯誤'}), 500


@noti_bp.route('/update/<int:notification_id>', methods=['POST'])
@login_required
def update_notification(notification_id):
    title = request.form.get('title', '').strip()
    content = request.form.get('content', '').strip()

    if not title or not content:
        return jsonify({'status': 'error', 'message': '標題與內容不可為空'}), 400

    updated_notif = Notification.update_notification(notification_id, title, content)
    if updated_notif:
        return jsonify({
            'status': 'success', 
            'message': '公告已更新',
            'notificationID': updated_notif.notificationID,
            'title': updated_notif.title,
            'content': updated_notif.content
        })
    else:
        return jsonify({'status': 'error', 'message': '找不到該公告'}), 404


@noti_bp.route('/delete/<int:notification_id>', methods=['POST'])
@login_required
def delete_notification(notification_id):
    result = Notification.delete_notification(notification_id)
    if result:
        return jsonify({'status': 'success', 'message': '公告已刪除'})
    else:
        return jsonify({'status': 'error', 'message': '找不到該公告'}), 404
