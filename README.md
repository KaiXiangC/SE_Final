# SE_Final
 2024Fall_SE_FinalProject 

 step 1
Step2

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