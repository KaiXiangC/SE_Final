from .. import db

class Notification(db.Model):
    __tablename__ = 'notification'
    notificationID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    createTime = db.Column(db.DateTime, nullable=False)  # Renamed from notificationTime
    updateTime = db.Column(db.DateTime, nullable=True)  # Added updateTime column
    title = db.Column(db.String(255), nullable=False)  # Added title column
    content = db.Column(db.String(1024), nullable=False)
