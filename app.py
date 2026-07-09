import os
import logging
import stripe
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize database
from database import init_db
db = init_db(app)

# Configure Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

# Import models after database initialization
from models import (
    User, Flight, Booking, Seat, Snack,
    create_test_data, get_user_by_id, get_user_by_email,
    get_flight_by_id, get_flights, get_booking_by_id, get_user_bookings,
    add_user, add_booking, get_available_seats, get_monthly_stats
)

from forms import LoginForm, RegisterForm, FlightSearchForm
from utils import login_required, admin_required, calculate_total

# Create database tables and test data
with app.app_context():
    db.create_all()
    create_test_data()

# Routes
@app.route('/')
def index():
    form = FlightSearchForm()
    return render_template('index.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        # Check if email already exists
        if get_user_by_email(form.email.data):
            flash('Email already registered', 'danger')
            return render_template('register.html', form=form)
        
        # Hash password and create user
        password_hash = generate_password_hash(form.password.data)
        user_id = add_user(form.name.data, form.email.data, password_hash)
        
        # Log user in
        session['user_id'] = user_id
        flash('Registration successful!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = get_user_by_email(form.email.data)
        
        if user and check_password_hash(user.password, form.password.data):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            
            # Redirect admins to admin dashboard
            if user.is_admin:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/flights', methods=['GET', 'POST'])
def search_flights():
    form = FlightSearchForm()
    now = datetime.now()
    
    if request.method == 'POST' and form.validate():
        departure = form.departure.data
        destination = form.destination.data
        date = form.date.data
        
        # Format date for searching
        if isinstance(date, datetime):
            date = date.strftime('%Y-%m-%d')
        
        # Get matching flights
        available_flights = Flight.query.filter(
            Flight.departure.ilike(f"%{departure}%"),
            Flight.destination.ilike(f"%{destination}%"),
            Flight.date == date
        ).all()
        
        return render_template(
            'flights.html', 
            flights=available_flights, 
            form=form,
            now=now
        )
    
    # If GET request or invalid form, show all flights
    all_flights = get_flights()
    return render_template('flights.html', flights=all_flights, form=form, now=now)

@app.route('/flight/<int:flight_id>')
def flight_details(flight_id):
    flight = get_flight_by_id(flight_id)
    if not flight:
        flash('Flight not found', 'danger')
        return redirect(url_for('search_flights'))
    
    return render_template('flights.html', flight=flight)

@app.route('/select-seat/<int:flight_id>')
@login_required
def select_seat(flight_id):
    flight = get_flight_by_id(flight_id)
    if not flight:
        flash('Flight not found', 'danger')
        return redirect(url_for('search_flights'))
    
    available_seats = get_available_seats(flight_id)
    
    return render_template(
        'seat_selection.html', 
        flight=flight, 
        available_seats=available_seats
    )

@app.route('/select-snacks/<int:flight_id>/<seat_code>')
@login_required
def select_snacks(flight_id, seat_code):
    flight = get_flight_by_id(flight_id)
    if not flight:
        flash('Flight not found', 'danger')
        return redirect(url_for('search_flights'))
    
    # Store the selected seat in the session
    session['selected_flight'] = flight_id
    session['selected_seat'] = seat_code
    
    # Get all snacks
    all_snacks = Snack.query.all()
    
    return render_template('snacks.html', flight=flight, snacks=all_snacks, seat=seat_code)

@app.route('/review-booking', methods=['POST'])
@login_required
def review_booking():
    # Get selected flight and seat from session
    flight_id = session.get('selected_flight')
    seat_code = session.get('selected_seat')
    
    if not flight_id or not seat_code:
        flash('Please select a flight and seat first', 'danger')
        return redirect(url_for('search_flights'))
    
    flight = get_flight_by_id(flight_id)
    
    # Get all snacks
    all_snacks = Snack.query.all()
    
    # Get selected snacks
    selected_snacks = []
    snack_total = 0
    
    for snack in all_snacks:
        quantity = int(request.form.get(f'snack_{snack.id}', 0))
        if quantity > 0:
            snack_item = {
                'id': snack.id,
                'name': snack.name,
                'price': snack.price,
                'quantity': quantity,
                'subtotal': quantity * snack.price
            }
            selected_snacks.append(snack_item)
            snack_total += snack_item['subtotal']
    
    # Store selections in session
    session['selected_snacks'] = selected_snacks
    
    # Find seat price
    seat_price = 0
    for seat_row in get_available_seats(flight_id):
        for seat in seat_row['seats']:
            if seat['code'] == seat_code:
                seat_price = seat['price']
                break
    
    total = flight.price + seat_price + snack_total
    
    # Store total in session
    session['booking_total'] = total
    
    return render_template(
        'payment.html',
        flight=flight,
        seat_code=seat_code,
        seat_price=seat_price,
        snacks=selected_snacks,
        snack_total=snack_total,
        total=total
    )

@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    flight_id = session.get('selected_flight')
    seat_code = session.get('selected_seat')
    total = session.get('booking_total', 0)
    
    if not flight_id or not seat_code or total <= 0:
        flash('Invalid booking information', 'danger')
        return redirect(url_for('index'))
    
    flight = get_flight_by_id(flight_id)
    
    try:
        YOUR_DOMAIN = request.host_url.rstrip('/')
        
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"Flight: {flight.flight_number} - {flight.departure} to {flight.destination}",
                        'description': f"Seat: {seat_code}, Date: {flight.date}, Time: {flight.time}",
                    },
                    'unit_amount': int(total * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + url_for('payment_success'),
            cancel_url=YOUR_DOMAIN + url_for('payment_cancel'),
        )
        
        # Store checkout session ID in session
        session['checkout_session_id'] = checkout_session.id
        
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        app.logger.error(f"Error creating checkout session: {str(e)}")
        flash('Payment processing error: ' + str(e), 'danger')
        return redirect(url_for('index'))

@app.route('/payment/success')
@login_required
def payment_success():
    # Get booking details from session
    flight_id = session.get('selected_flight')
    seat_code = session.get('selected_seat')
    selected_snacks = session.get('selected_snacks', [])
    user_id = session.get('user_id')
    
    if not flight_id or not seat_code or not user_id:
        flash('Invalid booking information', 'danger')
        return redirect(url_for('index'))
    
    # Create booking record
    booking_id = add_booking(
        user_id=user_id,
        flight_id=flight_id,
        seat_code=seat_code,
        snacks=selected_snacks,
        total=session.get('booking_total', 0),
        payment_status='completed'
    )
    
    # Clear booking data from session
    session.pop('selected_flight', None)
    session.pop('selected_seat', None)
    session.pop('selected_snacks', None)
    session.pop('booking_total', None)
    session.pop('checkout_session_id', None)
    
    flash('Booking successful! Your e-ticket has been confirmed.', 'success')
    
    # Get booking details for confirmation page
    booking = get_booking_by_id(booking_id)
    flight = get_flight_by_id(booking.flight_id)
    
    return render_template('confirmation.html', booking=booking, flight=flight)

@app.route('/payment/cancel')
@login_required
def payment_cancel():
    flash('Payment was cancelled. Please try again.', 'warning')
    
    # Clear booking session data
    session.pop('checkout_session_id', None)
    
    # We'll keep the booking details in case the user wants to try again
    flight_id = session.get('selected_flight')
    return redirect(url_for('select_seat', flight_id=flight_id))

@app.route('/my-bookings')
@login_required
def my_bookings():
    user_id = session.get('user_id')
    user_bookings = get_user_bookings(user_id)
    
    return render_template('user_bookings.html', bookings=user_bookings)

# Admin routes
@app.route('/admin')
@admin_required
def admin_dashboard():
    stats = get_monthly_stats()
    return render_template('admin/dashboard.html', stats=stats)

@app.route('/admin/reports')
@admin_required
def admin_reports():
    # Get monthly stats
    monthly_stats = get_monthly_stats()
    
    # Get all flights and bookings for detailed reporting
    all_flights = get_flights()
    all_bookings = Booking.query.all()
    
    return render_template(
        'admin/reports.html',
        monthly_stats=monthly_stats,
        flights=all_flights,
        bookings=all_bookings
    )

@app.route('/admin/flights')
@admin_required
def admin_flights():
    all_flights = get_flights()
    return render_template('admin/manage_flights.html', flights=all_flights)

@app.route('/admin/users')
@admin_required
def admin_users():
    all_users = User.query.all()
    return render_template('admin/manage_users.html', users=all_users)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)