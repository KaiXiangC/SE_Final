# app/models/vote.py
from app import db


class Vote(db.Model):
    __tablename__ = 'vote'
    voteID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'), nullable=False)
    voteTime = db.Column(db.DateTime, nullable=False)
    voteOption = db.Column(db.String(255), nullable=True)

    @classmethod
    def get_voted_issues_by_user(cls, user_id):
        from app.models.issue import Issue
        from app.models.vote import Vote
        return db.session.query(Issue) \
            .join(Vote, Issue.issueID == Vote.issueID) \
            .filter(Vote.userID == user_id).all()