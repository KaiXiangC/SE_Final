# app/models/issue.py
from app import db

class Issue(db.Model):
    __tablename__ = 'issue'
    issueID = db.Column(db.Integer, primary_key=True)
    categoryID = db.Column(db.Integer, db.ForeignKey('category.categoryID'), nullable=False)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    publishTime = db.Column(db.DateTime, nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    attachment_1 = db.Column(db.String(255), nullable=True)
    attachment_2 = db.Column(db.String(255), nullable=True)
    is_review = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)

    favorites = db.relationship('Favorite', backref='issue', lazy=True)
    votes = db.relationship('Vote', backref='issue', lazy=True)
    comments = db.relationship('Comment', backref='issue', lazy=True)

    @classmethod
    def get_posted_issues_by_user(cls, user_id):
        from app.models import Issue, Comment, Favorite, Vote
        return cls.query.filter_by(userID=user_id).all()