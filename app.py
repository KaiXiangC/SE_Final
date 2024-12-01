from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Issue
from forms.registration_form import RegistrationForm, IssueForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=form.password.data)
        form.photo.data.save(f'static/uploads/{user.name}_id.jpg')  # Save uploaded photo
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)
'''
@app.route('/new_issue', methods=['GET', 'POST'])
def new_issue():
    form = IssueForm()
    if form.validate_on_submit():
        issue = Issue(name=form.name.data, description=form.description.data, category=form.category.data)
        db.session.add(issue)
        db.session.commit()
        flash('Issue submitted successfully!', 'success')
        return redirect(url_for('home'))
    return render_template('new_issue.html', form=form)
'''
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    app.run(debug=True)
