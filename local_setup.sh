#!/bin/bash
# Setup script for local development with XAMPP

# Check if XAMPP is running
echo "Checking if XAMPP is running..."
if ! curl -s http://localhost/phpmyadmin/ > /dev/null; then
    echo "Error: XAMPP is not running. Please start Apache and MySQL services."
    exit 1
fi

echo "XAMPP is running."

# Set environment variables for MySQL
export USE_MYSQL=true
export MYSQL_DB=flight_booking
export MYSQL_USER=root
export MYSQL_PASSWORD=''  # Default XAMPP has no password
export MYSQL_HOST=localhost

# Ask for Stripe API key
read -p "Enter your Stripe Secret Key (or press Enter to skip): " stripe_key
if [ ! -z "$stripe_key" ]; then
    export STRIPE_SECRET_KEY=$stripe_key
    echo "Stripe API key set."
else
    echo "No Stripe API key provided. Payment features will not work."
fi

# Setup the database
echo "Setting up the database..."
python xampp_setup.py

# Start the application
echo "Starting the application..."
python main.py