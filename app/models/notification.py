from .. import db

class Notification(db.Model):
    __tablename__ = 'notification'
    notificationID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    notificationTime = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.String(1024), nullable=False)
