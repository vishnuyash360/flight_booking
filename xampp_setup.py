#!/usr/bin/env python3
"""
MySQL Database Setup Script for XAMPP Local Development

This script creates the necessary database schema and initial data for the
flight booking system when using MySQL with XAMPP.

Usage:
1. Make sure XAMPP MySQL server is running
2. Create a database named 'flight_booking' in phpMyAdmin
3. Run this script: python xampp_setup.py

The script will:
- Create all required tables
- Populate initial test data
"""

import os
import sys
import random
from datetime import datetime
from werkzeug.security import generate_password_hash

# Set environment variables for MySQL connection
os.environ['USE_MYSQL'] = 'true'
os.environ['MYSQL_USER'] = 'root'  # Default XAMPP MySQL username
os.environ['MYSQL_PASSWORD'] = ''   # Default XAMPP MySQL password (empty)
os.environ['MYSQL_HOST'] = 'localhost'
os.environ['MYSQL_DB'] = 'flight_booking'

# Create a Flask application context
try:
    from flask import Flask
    from database import init_db
    
    # Initialize a minimal Flask app for database setup
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database
    db = init_db(app)
    
    # Import models within app context to avoid circular imports
    with app.app_context():
        from models import (User, Flight, Booking, Seat, Snack, create_test_data)
        
        # Create tables
        print("Creating database tables...")
        db.create_all()
        
        # Create test data
        print("Populating test data...")
        create_test_data()
        
        print("Database setup completed successfully!")
        print("\nYou can now run the application with:")
        print("export USE_MYSQL=true")
        print("export MYSQL_DB=flight_booking")
        print("python main.py")
        
except ImportError as e:
    print(f"Error: {e}")
    print("Please make sure Flask and other dependencies are installed.")
    print("Run: pip install flask flask-sqlalchemy werkzeug")
    sys.exit(1)
except Exception as e:
    print(f"Error setting up database: {e}")
    print("\nTroubleshooting tips:")
    print("1. Make sure XAMPP MySQL server is running")
    print("2. Create a database named 'flight_booking' in phpMyAdmin")
    print("3. Check that username/password are correct (default: root/'')")
    sys.exit(1)