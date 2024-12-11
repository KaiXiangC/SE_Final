from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, LoginManager
from app import db
from app.models.issue import Issue

propose_bp = Blueprint('propose', __name__)

@propose_bp.route('/propose', methods=['GET', 'POST'])
@login_required
def propose():
        """新增問題"""
        if request.method == 'POST':
            title = request.form['title']
            description = request.form['description']
            new_issue = Issue(
                title=title,
                description=description,
                user_id=current_user.userID
            )
            
            try:
                db.session.add(new_issue)
                db.session.commit()
                flash('問題已新增', 'success')
                return redirect(url_for('home'))
            except:
                db.session.rollback()
                flash('新增問題失敗', 'danger')
        
        return render_template('propose.html')