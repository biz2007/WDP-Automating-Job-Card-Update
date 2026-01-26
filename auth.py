from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os

auth = Blueprint('auth', __name__)

# Users data storage
USERS_FILE = "users_data.json"

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def get_user_by_username(username):
    """Get user by username"""
    users = load_users()
    return next((u for u in users if u['username'].lower() == username.lower()), None)

def get_user_by_id(user_id):
    """Get user by ID"""
    users = load_users()
    return next((u for u in users if u['id'] == user_id), None)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()
        
        # Validation
        if not username or not email or not password:
            flash('Please fill in all fields', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        # Check if user exists
        if get_user_by_username(username):
            flash('Username already exists', 'danger')
            return render_template('register.html')
        
        users = load_users()
        
        # Check if email exists
        if any(u['email'].lower() == email.lower() for u in users):
            flash('Email already registered', 'danger')
            return render_template('register.html')
        
        # Create new user
        new_user = {
            'id': max([u['id'] for u in users], default=0) + 1,
            'username': username,
            'email': email,
            'password': generate_password_hash(password),
            'role': 'user',
            'created_at': datetime.now().isoformat()
        }
        
        users.append(new_user)
        save_users(users)
        
        flash('Registration successful! Please login', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            flash('Please fill in all fields', 'danger')
            return render_template('login.html')
        
        user = get_user_by_username(username)
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@auth.route('/logout')
def logout():
    """User logout"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Goodbye, {username}! You have been logged out', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/profile')
def profile():
    """User profile"""
    if 'user_id' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('auth.login'))
    
    user = get_user_by_id(session['user_id'])
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('auth.logout'))
    
    return render_template('profile.html', user=user)
