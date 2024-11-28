from .. import db

class Vote(db.Model):
    __tablename__ = 'vote'
    voteID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'), nullable=False)
    voteTime = db.Column(db.DateTime, nullable=False)
    voteOption = db.Column(db.String, nullable=False)
