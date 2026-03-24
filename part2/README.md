# HBnB Backend – Part 2

## Overview

This project implements the **backend core of the HBnB application**, a simplified Airbnb-like platform.
It follows a **layered architecture** using **Facade** and **Repository** patterns to separate concerns between API, business logic, and data persistence.

The system manages:

- Users
- Places
- Amenities
- Reviews

All entities inherit from a common base model and are stored using an **in-memory repository**.

---

## Project Architecture

The backend follows this architecture:

API Layer
↓
Service Layer (Facade)
↓
Persistence Layer (Repository)
↓
Models (Entities)


### API Layer
Handles HTTP requests using **Flask-RESTx**.

Responsibilities:
- Validate input data
- Define API endpoints
- Send responses to the client

### Service Layer (Facade)

The **HBnBFacade** acts as the central interface between the API and the persistence layer.

Responsibilities:
- Handle business logic
- Validate relationships between entities
- Coordinate operations across repositories

### Persistence Layer

Uses a **Repository pattern** with an `InMemoryRepository`.

Responsibilities:
- Store objects in memory
- Perform CRUD operations
- Retrieve objects by ID or attribute

### Models Layer

Defines the core entities of the application.

---

## Data Models

### BaseModel

Base class inherited by all models.

Attributes:

- `id` – unique UUID
- `created_at` – creation timestamp
- `updated_at` – last update timestamp

Methods:

- `save()` – updates timestamp
- `update(data)` – updates attributes
- `to_dict()` – converts object to dictionary for JSON responses

---

### User

Represents a system user.

Attributes:

- `first_name`
- `last_name`
- `email`
- `is_admin`

Validations:

- Names must be ≤ 50 characters
- Email must match a valid format

Relationships:

User 1 --- * Place
User 1 --- * Review

---

### Place

Represents a property listed in the platform.

Attributes:

- `title`
- `description`
- `price`
- `latitude`
- `longitude`
- `owner`

Validations:

- Title ≤ 100 characters
- Price must be positive
- Latitude between -90 and 90
- Longitude between -180 and 180

Relationships:

User 1 --- * Place
Place 1 --- * Review
Place * --- * Amenity

---

### Amenity

Represents a service available in a place.

Examples:

- WiFi
- Parking
- Pool
- Air conditioning

Attributes:

- `name`

Validation:

- Name required
- Maximum 50 characters

---

### Review

Represents feedback left by a user about a place.

Attributes:

- `text`
- `rating`
- `place`
- `user`

Validations:

- Text cannot be empty
- Rating must be between 1 and 5

Relationships:

User 1 --- * Review
Place 1 --- * Review

---

## API Endpoints

### Users

POST /users
GET /users
GET /users/<user_id>
PUT /users/<user_id>

---

### Places

POST /reviews
GET /reviews
GET /reviews/<review_id>
PUT /reviews/<review_id>
DELETE /reviews/<review_id>

---

### Amenities

POST /amenities
GET /amenities
GET /amenities/<amenity_id>
PUT /amenities/<amenity_id>

---

### Reviews

POST /reviews
GET /reviews
GET /reviews/<review_id>
PUT /reviews/<review_id>
DELETE /reviews/<review_id>

---

## Repository Pattern

The repository abstracts data storage operations.

Interface methods:

- `add(obj)`
- `get(id)`
- `get_all()`
- `update(id, data)`
- `delete(id)`
- `get_by_attribute(attr, value)`

Current implementation:

InMemoryRepository


Objects are stored in a Python dictionary.

---

## Design Patterns Used

### Facade Pattern

Provides a simplified interface to the system.

API → Facade → Repository


Benefits:

- Centralized business logic
- Cleaner API layer
- Easier maintenance

---

### Repository Pattern

Abstracts the data access layer.

Benefits:

- Decouples business logic from storage
- Allows easy replacement with a database later

---

## Data Flow Example

Creating a new Place:

Client Request
↓
API Endpoint
↓
HBnBFacade
↓
Validation of Owner and Amenities
↓
Place Model Creation
↓
Repository Storage
↓
JSON Response


---

## Technologies Used

- **Python**
- **Flask**
- **Flask-RESTx**
- **UUID**
- **In-Memory Storage**

---

## Future Improvements

- Replace `InMemoryRepository` with a real database
- Implement authentication (JWT)
- Add SQLAlchemy ORM
- Implement frontend integration

---

## Author

HBnB Backend Project - Selena Gómez & Alexander Zuleta
