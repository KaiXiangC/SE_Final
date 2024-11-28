from .. import db

class Admin(db.Model):
    __tablename__ = 'admin'
    adminID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
