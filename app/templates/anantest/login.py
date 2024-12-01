from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 資料庫模型
class User(db.Model):
    userID = db.Column(db.String(50), primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# 預設帳號密碼
default_account = {
    "email": "test@example.com",
    "password": "123456",
    "userID": "user001"
}

manager_account = {
    "email": "manager@example.com",
    "password": "manager123",
    "userID": "manager001"
}

# 初始化資料庫（首次運行時創建資料表）
with app.app_context():
    db.create_all()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # 查詢資料庫是否存在該 Email
        user = User.query.filter_by(email=email).first()

        # 驗證邏輯
        if user:  # 資料庫中有該使用者
            if user.password == password:
                session['userID'] = user.userID
                if user.userID == "manager001":
                    return redirect(url_for("manager_homepage"))
                return redirect(url_for("index"))
            else:
                error = "密碼錯誤，請重新輸入！"
        else:  # 當資料庫中沒有該帳號時，使用預設帳號驗證
            if email == default_account['email'] and password == default_account['password']:
                session['userID'] = default_account['userID']
                return redirect(url_for("index"))
            elif email == manager_account['email'] and password == manager_account['password']:
                session['userID'] = manager_account['userID']
                return redirect(url_for("manager_homepage"))
            else:
                error = "帳號或密碼錯誤，請重新輸入！"

        return render_template("login.html", error=error)

    return render_template("login.html")

@app.route("/")
def index():
    userID = session.get('userID', None)
    return f"歡迎使用者 {userID}！" if userID else "尚未登入，請先登入！"

@app.route("/manager_homepage")
def manager_homepage():
    return "這是管理者首頁！"

@app.route("/register")
def register():
    return "這是註冊頁面"

if __name__ == "__main__":
    app.run(debug=True)
