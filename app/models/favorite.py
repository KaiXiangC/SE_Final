# app/models/favorite.py
from app import db

class Favorite(db.Model):
    __tablename__ = 'favorite'
    favoriteID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    issueID = db.Column(db.Integer, db.ForeignKey('issue.issueID'), nullable=False)
    favoriteTime = db.Column(db.DateTime, nullable=False)

    @classmethod
    def get_favorited_issues_by_user(cls, user_id):
        from app.models.issue import Issue
        from app.models.favorite import Favorite
        return db.session.query(Issue) \
            .join(Favorite, Issue.issueID == Favorite.issueID) \
            .filter(Favorite.userID == user_id).all()