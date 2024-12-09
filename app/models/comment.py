# app/models/comment.py
from app import db


class Comment(db.Model):
    __tablename__ = 'comment'
    commentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'), nullable=False)
    commentTime = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_review = db.Column(db.Boolean, default=False)

    # 在 comment.py 中
    @classmethod
    def get_commented_issues_by_user(cls, user_id):
        from app.models.issue import Issue
        return db.session.query(Issue) \
            .join(cls, Issue.issueID == cls.issueID) \
            .filter(cls.userID == user_id).all()