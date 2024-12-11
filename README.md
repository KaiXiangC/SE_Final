# SE_Final
 2024Fall_SE_FinalProject 

## 前端頁面
登入頁面:login
註冊頁面:register
### 管理者端
管理員首頁:manager_homepage
議題討論與監控:propose_manage
審核留言review_comment
審核議題 review_issue
管理議題類別propose_category_manage.html
管理通知 maintenance_notice.html
### 使用者端
首頁 index.html
查看議題 propose.html
新增暫存議題 add_issue.html、finish_issue.html
議題頁面 issue_detail.html
用戶頁面usrProfile.html
通知usrNotification.html
變更密碼editPWD.html
修改用戶資料memberEdit.html


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
