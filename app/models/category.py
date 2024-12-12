from app import db

class Category(db.Model):
    __tablename__ = 'category'
    categoryID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    issues = db.relationship('Issue', backref='category', lazy=True)

    @classmethod
    def get_all_categories(cls):
        return cls.query.all()
