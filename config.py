import os

class Config:
    # 資料庫 URI (修改為您使用的資料庫)
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:OReEeDaejJYLSawJZIaOQTJPbYsOyXhO@junction.proxy.rlwy.net:29883/railway"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # 建議用環境變數設置