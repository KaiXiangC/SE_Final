from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import generate_password_hash
from app import db
from app.models import User
import logging
import os
from werkzeug.utils import secure_filename

register_bp = Blueprint('register', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
def register():
        """註冊"""
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            password = generate_password_hash(request.form['password'])
            idPhoto = ""
            profileData = ""
            idPhoto_filename = ""
            profileData_filename = ""
            authenticationStatus = False  # 'authenticationStatus' in request.form
            is_admin = False
            # 檢查電子郵件是否已存在
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                flash('此電子郵件已經註冊過!!', 'danger')
                return render_template('register.html')
        
            if email == 'admin@mail.com':
                is_admin = True
                authenticationStatus = True      

            else:
                # 儲存圖片檔案
                idPhoto = request.files['id_front']
                profileData = request.files['id_back']
                idPhoto_fname = secure_filename(idPhoto.filename)
                profileData_fname = secure_filename(profileData.filename)
                idPhoto.save(os.path.join(current_app.root_path, 'static/img', idPhoto_fname))
                profileData.save(os.path.join(current_app.root_path, 'static/img', profileData_fname))

            
            new_user = User(
                name=name,
                email=email,
                password=password,
                idPhoto=idPhoto_fname,
                authenticationStatus=authenticationStatus,
                profileData=profileData_fname,
                is_admin=is_admin
            )
            logging.error(f"錯誤")
            try:
                db.session.add(new_user)
                db.session.commit()
                flash('註冊成功', 'success')
                return redirect(url_for('login.login'))
            except Exception as e:
                db.session.rollback()
                logging.error(f"註冊失敗: {e}")
                flash(f'註冊失敗: {e}', 'danger')
                return render_template('register.html')
        
        return render_template('register.html')