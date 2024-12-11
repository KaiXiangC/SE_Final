from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import db
import app
from app.models.user import User
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
            if email == 'admin@mail.com':
                is_admin = True
                authenticationStatus = True      

            else:
                # 儲存圖片檔案
                idPhoto = request.files['id_front']
                profileData = request.files['id_back']
                idPhoto_fname = secure_filename(idPhoto.filename)
                profileData_fname = secure_filename(profileData.filename)
                idPhoto.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], idPhoto_fname))
                profileData.save(os.path.join(app.config["UPLOADED_PHOTOS_DEST"], profileData_fname))

            
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
                return redirect(url_for('login'))
            except Exception as e:
                db.session.rollback()
                logging.error(f"註冊失敗: {e}")
                flash('註冊失敗', 'danger')
        
        return render_template('register.html')