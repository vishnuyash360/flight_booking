from functools import wraps
from flask import session, redirect, url_for, flash
from models import get_user_by_id

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page', 'warning')
            return redirect(url_for('login'))
        
        user = get_user_by_id(session['user_id'])
        if not user or not user.is_admin:
            flash('You do not have permission to access this page', 'danger')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function

def calculate_total(flight_price, seat_price, snacks):
    """Calculate the total price of a booking."""
    snack_total = sum(snack['price'] * snack['quantity'] for snack in snacks)
    return flight_price + seat_price + snack_total