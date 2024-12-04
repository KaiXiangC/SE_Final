# SE_Final
 2024Fall_SE_FinalProject 


## 環境建置
```
pip install -r requirements.txt # 有改過其中一套件版本
pip install Flask-WTF
pip install flask-login
pip install --upgrade flask werkzeug
pip install pytest # 測試組的裝

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


## Convenience Prompt
專案檔案結構:
|   app.py
|   config.py
|   README.md
|   requirements.txt
|
+---.vscode
|       settings.json
|
+---app
|   |   __init__.py
|   |
|   +---forms
|   |   |   registration_form.py
|   |   |
|   |
|   +---models
|   |   |   category.py
|   |   |   comment.py
|   |   |   favorite.py
|   |   |   issue.py
|   |   |   notification.py
|   |   |   user.py
|   |   |   vote.py
|   |   |   __init__.py
|   |   |
|   |
|   +---routes
|   |   |   main.py
|   |   |   routes.py
|   |   |
|   |
|   +---templates
|   |   |   gotopropose.html
|   |   |   index.html
|   |   |   login.html
|   |   |   maintenance_notice.html
|   |   |   member.html
|   |   |   member_auth.html
|   |   |   member_homepage.html
|   |   |   member_manage.html
|   |   |   propose.html
|   |   |   propose_category_manage.html
|   |   |   propose_manage.html
|   |   |   register.html
|   |   |   review_comment.html
|   |   |   review_issue.html
|   |   |   seconded.html
|   |   |
|   |   \---anantest
|   |           app.py
|   |           auth.py
|   |           propose_manage.py
|   |           review_comment.py
|   |           review_issue.py
|   |
|
+---instance
|       app.db
|
+---migrations
|   +---versions
