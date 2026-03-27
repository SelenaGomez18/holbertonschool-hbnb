# HBnB - Full Stack Web Application

## Overview

HBnB is a full-stack web application inspired by Airbnb. The project is developed in multiple stages, progressively building a complete system that includes backend architecture, RESTful APIs, database persistence, authentication, and a simple web client.

The goal of the project is to understand how a real web application is structured using layered architecture, clean code principles, and modern web technologies.

---

# Project Architecture

The project follows a **layered architecture** to separate responsibilities and keep the code modular and maintainable.

### 1. Presentation Layer

Handles communication with the client.

* RESTful API endpoints
* HTTP request/response handling
* Authentication using JWT
* Frontend web client (HTML, CSS, JavaScript)

### 2. Business Logic Layer

Contains the core application logic.

* Entity validation
* Data processing
* Application rules
* Facade pattern to simplify interactions between layers

### 3. Persistence Layer

Responsible for storing and retrieving data.

* Repository pattern
* SQLAlchemy ORM
* Database models
* CRUD operations

---

# Technologies Used

### Backend

* Python 3
* Flask
* Flask-RESTX
* Flask-JWT-Extended
* SQLAlchemy
* SQLite

### Frontend

* HTML5
* CSS3
* JavaScript
* Fetch API
* DOM Manipulation

### Other Tools

* JWT Authentication
* Mermaid.js (ER diagrams)
* Git / GitHub
* REST API testing with cURL

---

# Project Structure

```
hbnb/
│
├── part1/          # Project architecture and core design
├── part2/          # API implementation and in-memory persistence
├── part3/          # Database integration with SQLAlchemy
├── part4/          # Simple web client (frontend)
│
└── README.md
```

---

# Core Entities

The application is built around the following main entities:

### User

Represents a user of the system.

Attributes:

* id
* first_name
* last_name
* email
* password
* is_admin

### Place

Represents a property listed by a user.

Attributes:

* id
* title
* description
* price
* owner (User)

### Review

Represents a review left by a user for a place.

Attributes:

* id
* text
* rating
* user_id
* place_id

### Amenity

Represents additional features offered by a place.

Examples:

* WiFi
* Pool
* Parking
* Air Conditioning

---

# Database Design

In **Part 3**, the application introduces a relational database using **SQLAlchemy**.

The database schema includes relationships between entities:

* A **User** can own multiple **Places**
* A **Place** can have multiple **Reviews**
* A **User** can write multiple **Reviews**
* A **Place** can have multiple **Amenities**

Entity relationships are represented using **ER diagrams generated with Mermaid.js**.

---

# Authentication

The application implements authentication using **JSON Web Tokens (JWT)**.

Main features:

* Secure login system
* Token generation after authentication
* Protected endpoints
* Cookie-based token storage in the frontend

---

# API Endpoints

The backend exposes RESTful endpoints such as:

```
POST   /api/v1/auth/login
GET    /api/v1/places
GET    /api/v1/places/{id}
POST   /api/v1/places
PUT    /api/v1/places/{id}
GET    /api/v1/reviews
POST   /api/v1/reviews
```

These endpoints allow interaction with the application's resources through HTTP requests.

---

# Frontend (Part 4)

The frontend is a simple web client built with:

* HTML
* CSS
* JavaScript

Features include:

* Login page
* Display list of places
* View place details
* Submit reviews
* Dynamic content loading using the Fetch API
* Authentication using JWT cookies

Main pages:

```
index.html       # List of places
login.html       # User login
place.html       # Place details and reviews
add_review.html  # Add a review
```

---

# Running the Project

### 1. Clone the repository

```
git clone https://github.com/yourusername/hbnb.git
cd hbnb
```

### 2. Create a virtual environment

```
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the application

```
python run.py
```

The server will start at:

```
http://localhost:5000
```

---

# Learning Objectives

Through this project, students learn how to:

* Design scalable backend architectures
* Implement RESTful APIs
* Apply the Repository and Facade patterns
* Use SQLAlchemy ORM with relational databases
* Implement authentication with JWT
* Connect a frontend client with a backend API
* Structure a full-stack web application

---

# Authors

**Selena Gómez & Alexander Zuleta**.
