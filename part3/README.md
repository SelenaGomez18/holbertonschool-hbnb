# HBnB - Part 3: Database & Authentication

## Overview

This project is part of the HBnB application backend.
Part 3 introduces **database persistence with SQLAlchemy**, **JWT authentication**, and **secure user management**.

The system exposes a RESTful API that allows managing users, places, reviews, and amenities.

---

## Technologies

* Python 3
* Flask
* Flask-RESTX
* SQLAlchemy
* Flask-JWT-Extended
* Flask-Bcrypt
* SQLite (development)

---

## Project Structure

```
hbnb/
│
├── app/
│   ├── api/v1/          # API endpoints
│   ├── models/          # SQLAlchemy models
│   ├── services/        # Facade layer
│   ├── utils/           # decorators and helpers
│   ├── extensions.py    # Flask extensions
│   └── __init__.py      # App factory
│
├── config.py            # Application configuration
├── run.py               # Application entry point
└── README.md
```

---

## Features

### Authentication

* JWT-based authentication
* Secure password hashing with bcrypt
* Token expiration management

### Users

* Create users
* Update user information
* Retrieve user data

### Places

* Create and manage places
* Link places to owners

### Reviews

* Users can review places
* Users cannot review their own place
* One review per user per place

### Amenities

* Manage amenities
* Many-to-many relationship with places

---

## Database Models

The application uses SQLAlchemy models:

* **User**
* **Place**
* **Review**
* **Amenity**

Relationships include:

* User → Places (one-to-many)
* User → Reviews (one-to-many)
* Place → Reviews (one-to-many)
* Place ↔ Amenities (many-to-many)

---

## Installation

Clone the repository:

```bash
git clone <repository_url>
cd hbnb
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the server:

```bash
python3 run.py
```

The API will run at:

```
http://127.0.0.1:5000
```

---

## API Endpoints

Examples:

```
POST   /api/v1/users
GET    /api/v1/users
GET    /api/v1/users/<id>

POST   /api/v1/reviews
GET    /api/v1/reviews
PUT    /api/v1/reviews/<id>
DELETE /api/v1/reviews/<id>
```

Some endpoints require **JWT authentication**.

---

## Security Rules

* Passwords are hashed using bcrypt
* JWT tokens protect restricted routes
* Only owners or admins can modify protected resources

---

## Author

HBnB Project – Selena Gómez & Alexander Zuleta
