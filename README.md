# SE_Final
 2024Fall_SE_FinalProject 


## 環境建置
```
pip install -r requirements.txt # 有改過其中一套件版本
pip install Flask-WTF
pip install flask-login
pip install pytest

```

安裝後即可在`SE_Final`目錄下執行
python app.py

## 資料庫創建流程
1. 如果沒有創立過 DB 先初始化 
```
flask db init   
```
2. 修改後 migrate
```
 flask db migrate 
```
3. 更新 DB 
```
flask db upgrade 
```
4. 創建後的 DB 會在 /instance
