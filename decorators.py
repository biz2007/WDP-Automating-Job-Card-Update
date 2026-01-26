from functools import wraps
from flask import session, flash, redirect, url_for

def login_required(f):
    """Decorator to require login for all users"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'admin':
            flash('Admin privileges required', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    """Decorator to allow only regular users (not admin)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('auth.login'))
        if session.get('role') != 'user':
            flash('User privileges required', 'danger')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function
