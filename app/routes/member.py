from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from flask_login import login_required, current_user, LoginManager
from app import db
from app.models.user import User
import logging

# 設置日誌記錄
logging.basicConfig(level=logging.DEBUG)

# login_manager = LoginManager()

member_bp = Blueprint('member', __name__)

@member_bp.route('/member/<int:user_id>', methods=['GET', 'POST'])
@login_required
def member(user_id):
        """會員資料"""
        if current_user.userID != user_id:
            flash('您無權訪問此頁面', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)
        
        return render_template('member.html', user=user)

@member_bp.route('/member/<int:user_id>/change_password', methods=['POST'])
@login_required
def change_password(user_id):
        """修改密碼"""
        if current_user.userID != user_id:
            flash('您無權修改此使用者的密碼', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)
        new_password = request.form['new-password']
        user.password = generate_password_hash(new_password)
        
        try:
            db.session.commit()
            flash('密碼已更新', 'success')
        except:
            db.session.rollback()
            flash('密碼更新失敗', 'danger')
        
        return redirect(url_for('member', user_id=user.userID))

@member_bp.route('/member/<int:user_id>/update_profile', methods=['POST'])
@login_required
def update_profile(user_id):
        """更新使用者資料"""
        if current_user.userID != user_id:
            flash('您無權修改此使用者的資料', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)
        user.name = request.form['name']
        user.email = request.form['email']
        user.idPhoto = request.form['idPhoto']
        user.authenticationStatus = 'authenticationStatus' in request.form
        user.profileData = request.form['profileData']
        
        try:
            db.session.commit()
            flash('資料已更新', 'success')
        except:
            db.session.rollback()
            flash('資料更新失敗', 'danger')
        
        return redirect(url_for('member', user_id=user.userID))

@member_bp.route('/member/<int:user_id>/editpwd', methods=['GET', 'POST'])
@login_required
def editpwd(user_id):
        if current_user.userID != user_id:
            flash('您無權訪問此頁面', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)

        return render_template('editPWD.html', user=user)

@member_bp.route('/member/<int:user_id>/memberedit', methods=['GET', 'POST'])
@login_required
def memberedit(user_id):
        if current_user.userID != user_id:
            flash('您無權訪問此頁面', 'danger')
            return redirect(url_for('login'))
        
        user = User.query.get_or_404(user_id)    
        
        return render_template('memberedit.html', user=user)