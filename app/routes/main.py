from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)
@main_bp.route('/')
def home():
        """首頁"""
        return render_template('login.html')