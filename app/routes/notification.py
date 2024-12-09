from flask import Blueprint, render_template, request
from flask_login import current_user
from app.models.notification import Notification
from app import db
from datetime import datetime
from flask_login import login_required, current_user

noti_bp = Blueprint('notification', __name__)

@noti_bp.route('/maintenance_notice', methods=['GET', 'POST'])
@login_required
def maintenance_notice():
    """維護通知"""
    if request.method == 'POST':
        content = request.form['content']
        new_notice = Notification(
            userID=current_user.userID,
            notificationTime=datetime.now(),
            content=content
        )
        
        try:
            db.session.add(new_notice)
            db.session.commit()
            flash('公告已發布', 'success')
        except:
            db.session.rollback()
            flash('公告發布失敗', 'danger')
    
    notices = Notification.query.order_by(Notification.notificationTime.desc()).all()
    return render_template('maintenance_notice.html', notices=notices)
