from datetime import datetime
from database import db
from werkzeug.security import generate_password_hash
import random
import os
import json

# Determine which database type we're using
# MySQL typically uses 'mysql' in the connection string
is_mysql = 'mysql' in os.environ.get('DATABASE_URL', '').lower()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    bookings = db.relationship('Booking', backref='user', lazy=True)

class Flight(db.Model):
    __tablename__ = 'flights'
    
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String(10), nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(10), nullable=False)
    time = db.Column(db.String(10), nullable=False)
    duration = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Float, nullable=False)
    aircraft = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Scheduled')
    
    bookings = db.relationship('Booking', backref='flight', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    seat_code = db.Column(db.String(5), nullable=False)
    # Handle JSON data differently for MySQL vs PostgreSQL
    _snacks = db.Column(db.Text, default='[]', nullable=False)
    total = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(20), default='pending')
    booking_date = db.Column(db.DateTime, default=datetime.now)
    
    @property
    def snacks(self):
        return json.loads(self._snacks)
    
    @snacks.setter
    def snacks(self, value):
        self._snacks = json.dumps(value)

class Seat(db.Model):
    __tablename__ = 'seats'
    
    id = db.Column(db.Integer, primary_key=True)
    row = db.Column(db.Integer, nullable=False)
    seat_class = db.Column(db.String(20), nullable=False)
    # Store JSON as text for compatibility
    _seats = db.Column(db.Text, nullable=False)
    
    @property
    def seats(self):
        return json.loads(self._seats)
    
    @seats.setter
    def seats(self, value):
        self._seats = json.dumps(value)

class Snack(db.Model):
    __tablename__ = 'snacks'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)

# Helper functions
def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def add_user(name, email, password):
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user.id

def get_flight_by_id(flight_id):
    return Flight.query.get(flight_id)

def get_flights():
    return Flight.query.all()

def get_booking_by_id(booking_id):
    return Booking.query.get(booking_id)

def get_user_bookings(user_id):
    return Booking.query.filter_by(user_id=user_id).all()

def add_booking(user_id, flight_id, seat_code, snacks, total, payment_status):
    booking = Booking(
        user_id=user_id,
        flight_id=flight_id,
        seat_code=seat_code,
        snacks=snacks,
        total=total,
        payment_status=payment_status
    )
    db.session.add(booking)
    db.session.commit()
    return booking.id

def get_available_seats(flight_id):
    # Get all seat data
    seat_data = Seat.query.all()
    
    # Get all booked seats for this flight
    booked_seats = [booking.seat_code for booking in Booking.query.filter_by(flight_id=flight_id).all()]
    
    # Create a copy of seats with availability
    available_seats = []
    for row in seat_data:
        seat_row = {
            'row': row.row,
            'class': row.seat_class,
            'seats': []
        }
        
        for seat in row.seats:
            seat_copy = seat.copy()
            seat_copy['available'] = seat['code'] not in booked_seats
            seat_row['seats'].append(seat_copy)
        
        available_seats.append(seat_row)
    
    return available_seats

def get_monthly_stats():
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Extract month and year in database-agnostic way
    if is_mysql:
        # MySQL syntax
        monthly_bookings = Booking.query.filter(
            db.text("MONTH(booking_date) = :month AND YEAR(booking_date) = :year")
        ).params(month=current_month, year=current_year).all()
    else:
        # PostgreSQL syntax
        monthly_bookings = Booking.query.filter(
            db.extract('month', Booking.booking_date) == current_month,
            db.extract('year', Booking.booking_date) == current_year
        ).all()
    
    # Group by flight
    flight_stats = {}
    for booking in monthly_bookings:
        flight_id = booking.flight_id
        if flight_id not in flight_stats:
            flight_stats[flight_id] = {
                'bookings': 0,
                'revenue': 0,
                'snacks_revenue': 0
            }
        
        flight_stats[flight_id]['bookings'] += 1
        flight_stats[flight_id]['revenue'] += booking.total
        
        # Calculate snack revenue
        snack_revenue = sum(snack['quantity'] * snack['price'] for snack in booking.snacks) if booking.snacks else 0
        flight_stats[flight_id]['snacks_revenue'] += snack_revenue
    
    # Format for display
    stats = []
    for flight_id, data in flight_stats.items():
        flight = get_flight_by_id(flight_id)
        if flight:
            stats.append({
                'flight_number': flight.flight_number,
                'route': f"{flight.departure} to {flight.destination}",
                'bookings': data['bookings'],
                'revenue': data['revenue'],
                'snacks_revenue': data['snacks_revenue'],
                'date': flight.date
            })
    
    return stats

# Create test data
def create_test_data():
    # Check if we already have data
    if User.query.count() > 0:
        return
    
    # Create admin user
    admin_password = generate_password_hash('admin123')
    admin = User(
        name='Admin User',
        email='admin@skyways.com',
        password=admin_password,
        is_admin=True
    )
    db.session.add(admin)
    
    # Create regular user
    user_password = generate_password_hash('password123')
    user = User(
        name='John Doe',
        email='user@example.com',
        password=user_password,
        is_admin=False
    )
    db.session.add(user)
    
    # Create flights
    destinations = ['New York', 'Los Angeles', 'Chicago', 'Miami', 'Dallas', 'Boston', 'San Francisco', 'Seattle']
    departures = ['Atlanta', 'Denver', 'Phoenix', 'Houston', 'Detroit', 'Philadelphia', 'Las Vegas', 'Charlotte']
    
    for i in range(1, 21):  # Create 20 flights
        flight_number = f"SK{1000 + i}"
        
        # Pick random departure and destination
        departure_idx = random.randint(0, len(departures) - 1)
        departure = departures[departure_idx]
        
        # Ensure destination is different from departure
        destination_options = [d for d in destinations if d != departure]
        destination = random.choice(destination_options)
        
        # Generate random date in next 30 days
        day = random.randint(1, 28)
        month = datetime.now().month
        year = datetime.now().year
        
        if month == 12 and day > datetime.now().day:
            month = 1
            year += 1
        
        flight_date = f"{year}-{month:02d}-{day:02d}"
        
        # Generate random time
        hour = random.randint(6, 22)
        minute = random.choice([0, 15, 30, 45])
        flight_time = f"{hour:02d}:{minute:02d}"
        
        # Generate random price between $150 and $600
        price = round(random.uniform(150, 600), 2)
        
        flight = Flight(
            flight_number=flight_number,
            departure=departure,
            destination=destination,
            date=flight_date,
            time=flight_time,
            duration=f"{random.randint(1, 5)}h {random.randint(0, 59)}m",
            price=price,
            aircraft=random.choice(['Boeing 737', 'Airbus A320', 'Boeing 787', 'Airbus A350']),
            status='Scheduled'
        )
        db.session.add(flight)
    
    # Create seat layout
    seat_letters = ['A', 'B', 'C', 'D', 'E', 'F']
    
    # First class (rows 1-2)
    for row in range(1, 3):
        seat_row_data = []
        
        for letter in seat_letters:
            # First class seats are more expensive
            price = 150.0
            seat_row_data.append({
                'code': f"{row}{letter}",
                'price': price,
                'class': 'First'
            })
        
        seat = Seat(
            row=row,
            seat_class='First',
            seats=seat_row_data
        )
        db.session.add(seat)
    
    # Business class (rows 3-7)
    for row in range(3, 8):
        seat_row_data = []
        
        for letter in seat_letters:
            # Business class seats pricing
            price = 100.0
            seat_row_data.append({
                'code': f"{row}{letter}",
                'price': price,
                'class': 'Business'
            })
        
        seat = Seat(
            row=row,
            seat_class='Business',
            seats=seat_row_data
        )
        db.session.add(seat)
    
    # Economy class (rows 8-20)
    for row in range(8, 21):
        seat_row_data = []
        
        for letter in seat_letters:
            # Economy class seats pricing
            if letter in ['A', 'F']:  # Window seats
                price = 50.0
            elif letter in ['C', 'D']:  # Middle seats
                price = 30.0
            else:  # Aisle seats
                price = 40.0
                
            seat_row_data.append({
                'code': f"{row}{letter}",
                'price': price,
                'class': 'Economy'
            })
        
        seat = Seat(
            row=row,
            seat_class='Economy',
            seats=seat_row_data
        )
        db.session.add(seat)
    
    # Create snacks
    snacks_data = [
        {
            'name': 'Premium Sandwich',
            'description': 'Gourmet sandwich with premium ingredients',
            'price': 12.99
        },
        {
            'name': 'Salad Bowl',
            'description': 'Fresh garden salad with dressing',
            'price': 10.99
        },
        {
            'name': 'Snack Box',
            'description': 'Assortment of crackers, cheese, and nuts',
            'price': 8.99
        },
        {
            'name': 'Fresh Fruit',
            'description': 'Selection of seasonal fresh fruits',
            'price': 7.99
        },
        {
            'name': 'Chips',
            'description': 'Gourmet potato chips',
            'price': 4.99
        },
        {
            'name': 'Chocolate Bar',
            'description': 'Premium chocolate',
            'price': 3.99
        },
        {
            'name': 'Bottled Water',
            'description': 'Pure spring water',
            'price': 2.99
        },
        {
            'name': 'Soft Drink',
            'description': 'Soda or juice',
            'price': 3.49
        },
        {
            'name': 'Coffee/Tea',
            'description': 'Fresh brewed coffee or tea',
            'price': 3.99
        },
        {
            'name': 'Wine',
            'description': 'Red or white wine (187ml)',
            'price': 9.99
        }
    ]
    
    for snack_data in snacks_data:
        snack = Snack(**snack_data)
        db.session.add(snack)
    
    # Commit all changes
    db.session.commit()