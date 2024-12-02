from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import db, User
from app.models.issue import Issue
from app.forms.registration_form import RegistrationForm, IssueForm
app = Flask(__name__, template_folder='app/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.route('/')
def home():
    return render_template('login.html')

#註冊
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        idPhoto = request.form['id_front_path']
        authenticationStatus = False #'authenticationStatus' in request.form
        profileData = request.form['id_back_path']
        
        new_user = User(
            name=name,
            email=email,
            password=password,
            idPhoto=idPhoto,
            authenticationStatus=authenticationStatus,
            profileData=profileData,
            is_admin=False
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('註冊成功', 'success')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('註冊失敗', 'danger')
    
    return render_template('register.html')

#新增問題
@app.route('/propose', methods=['GET', 'POST'])
def propose():
    form = IssueForm()
    if form.validate_on_submit():
        issue = Issue(name=form.name.data, description=form.description.data, category=form.category.data)
        db.session.add(issue)
        db.session.commit()
        flash('Issue submitted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('propose.html', form=form)

#會員
@app.route('/member/<int:user_id>', methods=['GET', 'POST'])
def member(user_id):
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.name = request.form['name']
        user.email = request.form['email']
        user.password = request.form['password']
        user.idPhoto = request.form['idPhoto']
        user.authenticationStatus = 'authenticationStatus' in request.form
        user.profileData = request.form['profileData']
        
        try:
            db.session.commit()
            flash('資料已更新', 'success')
        except:
            db.session.rollback()
            flash('更新失敗', 'danger')
        
        return redirect(url_for('member', user_id=user.id))
    
    return render_template('member.html', user=user)

#登入
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.userID
            flash('登入成功', 'success')
            return redirect(url_for('member', user_id=user.userID))
        else:
            flash('帳號或密碼錯誤', 'danger')
            return render_template('login.html', error='帳號或密碼錯誤')
    
    return render_template('login.html')
'''
@app.route('/api/proposals/latest', methods=['GET'])
def get_latest_proposals():
    proposals = Proposal.query.order_by(Proposal.date.desc()).limit(10).all()
    return jsonify([proposal.to_dict() for proposal in proposals])

@app.route('/api/proposals/popular', methods=['GET'])
def get_popular_proposals():
    proposals = Proposal.query.order_by(Proposal.support_count.desc()).limit(10).all()
    return jsonify([proposal.to_dict() for proposal in proposals])

@app.route('/api/proposals/completed', methods=['GET'])
def get_completed_proposals():
    proposals = Proposal.query.filter_by(status='completed').order_by(Proposal.date.desc()).limit(10).all()
    return jsonify([proposal.to_dict() for proposal in proposals])
'''
@app.route('/seconded', methods=['GET'])
def seconded():
    return render_template('seconded.html')


if __name__ == '__main__':
    with app.app_context():       
        db.create_all()  # Create tables
    app.run(debug=True)