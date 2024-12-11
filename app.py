from app import create_app, db
from sqlalchemy import text
import logging

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 檢查資料庫連接
        try:
            db.session.execute(text('SELECT 1'))
            logging.info("資料庫連接成功")
        except Exception as e:
            logging.error(f"資料庫連接失敗: {e}")

        db.create_all()  # Create tables

        # 設置圖片上傳
        app.config["UPLOADED_PHOTOS_DEST"] = "app/static/img"

    app.run(debug=True)