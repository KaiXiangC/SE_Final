from .. import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notification'
    notificationID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    createTime = db.Column(db.DateTime, nullable=False)  
    updateTime = db.Column(db.DateTime, nullable=True)  
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(1024), nullable=False)

    @classmethod
    def get_notifications_by_title(cls, title_keyword=None):
        query = cls.query
        if title_keyword:
            query = query.filter(cls.title.like(f"%{title_keyword}%"))
        return query.order_by(cls.createTime.desc()).all()
    
    @classmethod
    def create_notification(cls, user_id, title, content):
        new_notif = cls(
            userID=user_id,
            createTime=datetime.utcnow(),
            title=title,
            content=content
        )
        db.session.add(new_notif)
        db.session.commit()
        return new_notif

    @classmethod
    def update_notification(cls, notification_id, title, content):
        notif = cls.query.get(notification_id)
        if notif:
            notif.title = title
            notif.content = content
            notif.updateTime = datetime.utcnow()
            db.session.commit()
            return notif
        return None

    @classmethod
    def delete_notification(cls, notification_id):
        notif = cls.query.get(notification_id)
        if notif:
            db.session.delete(notif)
            db.session.commit()
            return True
        return False
    
    @classmethod
    def get_notifications_by_user(cls, user_id):
        return cls.query.filter_by(userID=user_id).all()
    
    @classmethod
    def get_admin_notifications(cls):
        from app.models.user import User
        """獲取唯一 is_admin 為 True 的用戶的所有通知。"""
        admin_user = User.query.filter_by(is_admin=True).first()
        if not admin_user:
            return []  # 如果沒有管理員，用空列表返回
        return cls.query.filter_by(userID=admin_user.userID).all()
    
    def to_dict(self):
        return {
            "title": self.title,
            "content": self.content,
            # 加上其他你需要的屬性
        }