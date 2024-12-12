from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
from app import db
import os
from app.models import User, Issue, Category
import logging

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/member_manage')
@login_required
def member_manage():
        """會員管理"""
        users = User.query.filter_by(is_admin=False).all()
        return render_template('member_manage.html', users=users)

@admin_bp.route('/propose_manage')
@login_required
def propose_manage():
        """議題管理"""
        return render_template('propose_manage.html')

@admin_bp.route('/propose_category_manage')
@login_required
def propose_category_manage():
        """議題類別管理"""
        categories = Category.query.all()
        return render_template('propose_category_manage.html', categories=categories)

@admin_bp.route('/add_category', methods=['POST'])
def add_category():
    """新增類別"""
    category_name = request.form['category_name']
    new_category = Category(name=category_name)
    try:
        db.session.add(new_category)
        db.session.commit()
        flash('類別新增成功', 'success')
    except Exception as e:
        db.session.rollback()
        flash('類別新增失敗', 'danger')
    return redirect(url_for('admin.propose_category_manage'))

@admin_bp.route('/delete_category',  methods=['POST', 'GET'])
def delete_category():
    """刪除類別"""
    category_id = request.form['category_id']
    category = Category.query.filter_by(categoryID=category_id).first()
    logging.error(f"category_id: {category_id}")
    if category:
        try:
            db.session.delete(category)
            db.session.commit()
            flash('類別刪除成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash('類別刪除失敗', 'danger')
    else:
        flash('類別不存在', 'danger')
    return redirect(url_for('admin.propose_category_manage'))

@admin_bp.route('/edit_category', methods=['POST'])
def edit_category():
    """修改類別"""
    category_id = request.form['category_id']
    new_category_name = request.form['newCategoryName']
    category = Category.query.get(category_id)
    if category:
        try:
            category.name = new_category_name
            db.session.commit()
            flash('類別修改成功', 'success')
        except Exception as e:
            db.session.rollback()
            flash('類別修改失敗', 'danger')
    else:
        flash('類別不存在', 'danger')
    return redirect(url_for('admin.propose_category_manage'))

@admin_bp.route('/member_auth/<int:user_id>', methods=['GET'])
@login_required
def member_auth(user_id):
    """會員審核"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.authenticationStatus = 'authenticationStatus' in request.form
        
        try:
            db.session.commit()
            flash('會員認證狀態已更新', 'success')
        except Exception as e:
            db.session.rollback()
            logging.error(f"會員認證狀態更新失敗: {e}")
            flash('會員認證狀態更新失敗', 'danger')
        
        return redirect(url_for('admin.member_manage'))
    
    return render_template('member_auth.html', user=user)

@admin_bp.route('/approve/<int:user_id>', methods=['GET'])
@login_required
def approve(user_id):
    """審核會員"""
    user = User.query.get_or_404(user_id)
    user.authenticationStatus = True
    
    try:
        db.session.commit()
        flash('會員已審核通過', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"會員審核失敗: {e}")
        flash('會員審核失敗', 'danger')
    
    return redirect(url_for('admin.member_manage'))

@admin_bp.route('/reject/<int:user_id>', methods=['GET'])
@login_required
def reject(user_id):
    """退件會員並刪除資料和圖片"""
    user = User.query.get_or_404(user_id)
    
    try:
        # 刪除圖片
        if user.idPhoto:
            id_photo_path = os.path.join(current_app.root_path, 'static/img', user.idPhoto)
            if os.path.exists(id_photo_path):
                os.remove(id_photo_path)
        
        if user.profileData:
            profile_data_path = os.path.join(current_app.root_path, 'static/img', user.profileData)
            if os.path.exists(profile_data_path):
                os.remove(profile_data_path)
        
        # 刪除會員資料
        db.session.delete(user)
        db.session.commit()
        flash('會員已退件並刪除資料和圖片', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"會員退件失敗: {e}")
        flash('會員退件失敗', 'danger')
    
    return redirect(url_for('admin.member_manage'))