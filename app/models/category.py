from app import db

class Category(db.Model):
    __tablename__ = 'category'
    categoryID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    issues = db.relationship('Issue', backref='category', lazy=True)
    
    @classmethod
    def get_uncategorized_category_id(cls):
        """
        Get the ID of the 'Uncategorized' category if it exists.
        """
        uncategorized = cls.query.filter_by(name='無類別').first()
        return uncategorized.categoryID if uncategorized else None
    
    @classmethod
    def get_all_categories(cls, exclude_uncategorized=True):
        """
        Get all categories, optionally excluding the 'Uncategorized' category.
        """
        query = cls.query
        if exclude_uncategorized:
            query = query.filter(cls.name != '無類別')
        return query.all()
    
