from .. import db

class Comment(db.Model):
    __tablename__ = 'comment'
    commentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'), nullable=False)
    commentTime = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
