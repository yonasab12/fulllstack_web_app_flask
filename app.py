#{% extends "base.html" %}
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('fresh'))
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            
            existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
            if existing_user:
                flash('Username or email already exists!', 'danger')
                return redirect(url_for('signup'))
            
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please login', 'success')
            return redirect(url_for('login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Error creating account. Please try again.', 'danger')
            app.logger.error(f"Signup error: {str(e)}")
            
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('fresh'))
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('fresh'))
            flash('Invalid credentials!', 'danger')
            
        except Exception as e:
            flash('Login error. Please try again.', 'danger')
            app.logger.error(f"Login error: {str(e)}")
            
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing'))

@app.route('/fresh')
@login_required
def fresh():
    return render_template('fresh.html')
# Add these routes
@app.route('/home')
@login_required
def home():
    return render_template('home.html')


# Add these routes
@app.route('/service')
@login_required
def service():
    return render_template('service.html')

@app.route('/note')
@login_required
def note():
    return render_template('note.html')
@app.route('/contact')
@login_required
def contact():
    return render_template('contact_us.html')

@app.route('/remedial')
@login_required
def remedial():
    return render_template('remedial.html')

@app.route('/quiz')
@login_required
def quiz():
    return render_template('quiz.html')
 # Add this line
@app.route('/story')
@login_required
def story():
    return render_template('story.html')
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
