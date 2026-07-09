-- MySQL Database Schema for Flight Booking System
-- For use with XAMPP local development

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS flight_booking;
USE flight_booking;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(256) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Flights table
CREATE TABLE IF NOT EXISTS flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_number VARCHAR(10) NOT NULL,
    departure VARCHAR(100) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    date VARCHAR(10) NOT NULL,
    time VARCHAR(10) NOT NULL,
    duration VARCHAR(10) NOT NULL,
    price FLOAT NOT NULL,
    aircraft VARCHAR(100) NOT NULL,
    status VARCHAR(20) DEFAULT 'Scheduled'
);

-- Seats table
CREATE TABLE IF NOT EXISTS seats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    row INT NOT NULL,
    seat_class VARCHAR(20) NOT NULL,
    _seats TEXT NOT NULL
);

-- Snacks table
CREATE TABLE IF NOT EXISTS snacks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(255) NOT NULL,
    price FLOAT NOT NULL
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    flight_id INT NOT NULL,
    seat_code VARCHAR(5) NOT NULL,
    _snacks TEXT DEFAULT '[]' NOT NULL,
    total FLOAT NOT NULL,
    payment_status VARCHAR(20) DEFAULT 'pending',
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);

-- Insert admin user
INSERT INTO users (name, email, password, is_admin)
VALUES (
    'Admin User',
    'admin@skyways.com',
    -- Password: admin123
    '$2b$12$tRIOaMOxfDY1xOp9WCWfsuT8aM9TMTQpgLJBZx49CpyK/KPPf7cUS',
    1
);

-- Insert regular user
INSERT INTO users (name, email, password, is_admin)
VALUES (
    'John Doe',
    'user@example.com',
    -- Password: password123
    '$2b$12$VXYQAHQpXzhpZjZ2z7YS0e5RQTvd3JytDKCU/xJx.zhf45w6mZQN2',
    0
);

-- Insert sample snacks
INSERT INTO snacks (name, description, price) VALUES
('Premium Sandwich', 'Gourmet sandwich with premium ingredients', 12.99),
('Salad Bowl', 'Fresh garden salad with dressing', 10.99),
('Snack Box', 'Assortment of crackers, cheese, and nuts', 8.99),
('Fresh Fruit', 'Selection of seasonal fresh fruits', 7.99),
('Chips', 'Gourmet potato chips', 4.99),
('Chocolate Bar', 'Premium chocolate', 3.99),
('Bottled Water', 'Pure spring water', 2.99),
('Soft Drink', 'Soda or juice', 3.49),
('Coffee/Tea', 'Fresh brewed coffee or tea', 3.99),
('Wine', 'Red or white wine (187ml)', 9.99);

-- Sample flights would be inserted here
-- For complete data, run the Python script which generates
-- more comprehensive test data with proper JSON formatting

-- Note: To run this script in phpMyAdmin:
-- 1. Open phpMyAdmin
-- 2. Select "SQL" tab
-- 3. Copy and paste this entire script
-- 4. Click "Go" to execute