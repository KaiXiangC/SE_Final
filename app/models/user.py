from .. import db


class User(db.Model):
    __tablename__ = 'user'
    userID = db.Column(db.Integer, primary_key=True)
    idPhoto = db.Column(db.LargeBinary, nullable=True)
    password = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    authenticationStatus = db.Column(db.Boolean, nullable=False, default=False)
    profileData = db.Column(db.LargeBinary, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    notifications = db.relationship('Notification', backref='user', lazy=True)
    favorites = db.relationship('Favorite', backref='user', lazy=True)
    issues = db.relationship('Issue', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)

    def get_id(self):
        return self.userID

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def retrieve_user_photo(self):
        # 從 User 表中根據 ID 查找記錄
        user = User.query.filter_by(id=self.userID).first()

        if user:
            if user.photo:  # 確認圖片資料存在
                return user.photo  # 返回圖片 BLOB 資料
            else:
                raise ValueError("No photo found for this user")
        else:
            raise ValueError("User not found")
