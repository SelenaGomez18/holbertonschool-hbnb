# HBnB Project – Part 4: Simple Web Client

## Overview

This project implements the **frontend client** of the HBnB application.
It interacts with the HBnB backend API to allow users to:

* Login using JWT authentication
* View available places
* View place details
* Read reviews
* Submit reviews (only authenticated users)

The frontend is built using **HTML, CSS, and JavaScript**, and communicates with the backend using the **Fetch API**.

---

# Features

## User Authentication

Users can log in using their email and password.

* The frontend sends a **POST request** to the backend authentication endpoint.
* If the login is successful, the API returns a **JWT token**.
* The token is stored in a **browser cookie** and used for authenticated requests.

---

## View Places

The main page (`index.html`) displays a list of available places.

The frontend:

1. Sends a **GET request** to the API:

```
GET /api/v1/places
```

2. Receives the places as JSON.

3. Dynamically generates **place cards** using JavaScript.

Each card shows:

* Place name
* Price per night
* Button to view details

---

## View Place Details

The **place details page** (`place.html`) displays detailed information about a specific place.

Steps:

1. The place ID is extracted from the URL query parameters.
2. A **GET request** is sent to:

```
GET /api/v1/places/{place_id}
```

3. The response includes:

* Name
* Description
* Price
* Reviews

4. JavaScript dynamically renders this data into the page.

---

## Reviews

Each place can have multiple reviews.

The reviews section displays:

* User name
* Rating
* Review text

If no reviews exist, a message is displayed.

---

## Add Review

Authenticated users can submit a review for a place.

The frontend:

1. Checks if the user is authenticated by verifying the **JWT token in cookies**.
2. Displays the **review form** only if the user is logged in.
3. Sends a **POST request** to the API:

```
POST /api/v1/reviews
```

Request body:

```
{
  "place_id": "PLACE_ID",
  "text": "Review text",
  "rating": 5
}
```

If the submission succeeds:

* A success message is shown.
* The review is added to the page dynamically.

---

# Project Structure

```
.
├── index.html
├── login.html
├── place.html
├── add_review.html
├── styles.css
├── scripts.js
└── images/
    └── logo.png
```

### Files Description

**index.html**

* Displays the list of available places.

**login.html**

* Login form for user authentication.

**place.html**

* Displays detailed information about a selected place.
* Shows reviews and review form.

**add_review.html**

* Page for submitting a review.

**styles.css**

* Contains all styling for layout, forms, cards, and responsive design.

**scripts.js**

* Contains all frontend logic including:

  * API requests
  * authentication
  * DOM manipulation
  * review submission

---

# Technologies Used

* **HTML5**
* **CSS3**
* **JavaScript (ES6)**
* **Fetch API**
* **JWT Authentication**
* **REST API**

---

# Authentication

Authentication uses **JWT tokens**.

Login flow:

1. User submits login form.
2. Frontend sends credentials to:

```
POST /api/v1/auth/login
```

3. Backend returns:

```
{
  "access_token": "JWT_TOKEN"
}
```

4. The token is stored in a **browser cookie**.

5. Authenticated requests include:

```
Authorization: Bearer TOKEN
```

---

# How to Run the Project

1. Start the **HBnB backend server**

```
python run.py
```

The backend runs on:

```
http://127.0.0.1:5000
```

2. Open the frontend pages in the browser:

```
index.html
```

3. Login with a valid user account.

4. Browse places and submit reviews.

---

# Learning Objectives

This part of the project focuses on:

* Frontend development
* API integration
* JWT authentication
* DOM manipulation
* Fetch API usage
* Dynamic content rendering

---

# Author

HBnB Project – Selena Gómez & Alexander Zuleta
