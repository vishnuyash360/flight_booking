# ✈️ Flight Booking Management System

A modern **Flight Booking Management System** built with **Flask**, **SQLAlchemy**, **PostgreSQL/MySQL**, and **Bootstrap**. The application allows users to search flights, book seats, manage reservations, and provides an admin dashboard for managing flights and bookings.

---

## 🚀 Features

### 👤 User Features

* User Registration & Login
* Secure Password Hashing
* Flight Search
* Flight Booking
* Seat Selection
* Snack Selection
* Booking Confirmation
* View Booking History
* Responsive User Interface

### 🛠️ Admin Features

* Admin Authentication
* Dashboard Overview
* Flight Management
* Booking Management
* Monthly Statistics
* Passenger Information
* Revenue Tracking

---

## 🖥️ Tech Stack

### Backend

* Python 3
* Flask
* Flask-SQLAlchemy
* WTForms
* SQLAlchemy ORM

### Frontend

* HTML5
* CSS3
* Bootstrap 5
* JavaScript

### Database

* PostgreSQL (Recommended)
* MySQL (Legacy Support)

### Payment

* Stripe API Integration

---

## 📂 Project Structure

```text
Flight-Booking-System/
│
├── app.py
├── main.py
├── database.py
├── models.py
├── forms.py
├── utils.py
│
├── templates/
├── static/
├── instance/
├── migrations/
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Flight-Booking-System.git
cd Flight-Booking-System
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/flight_booking

SESSION_SECRET=your_secret_key

STRIPE_SECRET_KEY=your_stripe_secret_key
```

---

### 5. Create PostgreSQL Database

```sql
CREATE DATABASE flight_booking;
```

---

### 6. Run the application

```bash
python main.py
```

The application will start on:

```
http://127.0.0.1:5010
```

---

## 📊 Database

The application uses **SQLAlchemy ORM**, making it easy to switch between supported databases.

Current models include:

* Users
* Flights
* Bookings
* Seats
* Snacks

---

## 🔒 Security

* Password Hashing
* Session-Based Authentication
* Role-Based Access Control
* Form Validation
* Secure Database Access

---

## 📸 Screenshots

You can add screenshots here:

* Home Page
* Login Page
* Flight Search
* Booking Page
* Admin Dashboard

---

## 🔮 Future Improvements

* Flight Cancellation
* Email Notifications
* Online Check-in
* Boarding Pass Generation
* Flight Status Tracking
* Multi-language Support
* PDF Ticket Generation
* Payment History
* REST API
* Docker Deployment

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 📄 License

This project is created for educational and learning purposes.

---

## 👨‍💻 Author

Developed by **Vishnu Pandey**

If you found this project useful, consider giving it a ⭐ on GitHub.
