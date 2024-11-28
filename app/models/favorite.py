from .. import db

class Favorite(db.Model):
    __tablename__ = 'favorite'
    favoriteID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'), nullable=False)
    favoriteTime = db.Column(db.DateTime, nullable=False)
