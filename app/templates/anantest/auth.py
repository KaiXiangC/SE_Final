@app.route("/approve/<userID>", methods=["GET"])
def approve(userID):
    # 查詢該用戶資料
    user = User.query.filter_by(userID=userID).first()

    if user:
        # 更新 authenticationStatus 為 true
        user.authenticationStatus = True
        db.session.commit()

    return redirect(url_for('member_manage'))  # 返回會員管理頁面

@app.route("/reject/<userID>", methods=["GET"])
def reject(userID):
    # 刪除該用戶資料
    user = User.query.filter_by(userID=userID).first()

    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect(url_for('member_manage'))  # 返回會員管理頁面
