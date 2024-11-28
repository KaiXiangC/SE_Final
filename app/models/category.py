from .. import db

class Category(db.Model):
    __tablename__ = 'category'
    categoryID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    issues = db.relationship('Issue', backref='category', lazy=True)
