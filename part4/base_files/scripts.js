let allPlaces = [];

// ----------- Helper Functions -----------
function getCookie(name) {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split("=");
        if (key === name) return value;
    }
    return null;
}

function checkAuthenticationRedirect() {
    const token = getCookie("token");
    if (!token) {
        window.location.href = "index.html";
        return null;
    }
    return token;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("place_id") || params.get("id");
}

// ----------- JWT Helper -----------
function parseJwt(token) {
    if (!token) return null;
    try {
        const base64Payload = token.split('.')[1];
        const payload = atob(base64Payload);
        return JSON.parse(payload);
    } catch (e) {
        console.error("Invalid JWT", e);
        return null;
    }
}

// ----------- Login -----------
async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        if (!response.ok) throw new Error("Login failed");
        const data = await response.json();

        document.cookie = `token=${data.access_token}; path=/`;
        window.location.href = "index.html";
    } catch (error) {
        console.error(error);
        alert("Login failed");
    }
}

// ----------- API Functions -----------
async function fetchPlaces() {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/places");
        if (!response.ok) throw new Error("Failed to fetch places");
        const places = await response.json();

        allPlaces = places; // guardar todos los places
        displayPlaces(places);

    } catch (error) {
        console.error(error);
    }
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = token ? { "Authorization": `Bearer ${token}` } : {};
        const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, { method: "GET", headers });
        if (!response.ok) throw new Error("Failed to fetch place details");

        const place = await response.json();
        displayPlaceDetails(place);
        if (place.reviews) displayReviews(place.reviews);
    } catch (error) {
        console.error(error);
    }
}

async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch("http://127.0.0.1:5000/api/v1/reviews/", {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${token}` },
            body: JSON.stringify({ place_id: placeId, text: reviewText, rating })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Failed to submit review");
        }

        alert("Review submitted successfully!");
        return true;
    } catch (error) {
        console.error(error);
        alert("Error submitting review: " + error.message);
        return false;
    }
}

// ----------- DOM Functions -----------
function displayPlaces(places) {
    const placesList = document.getElementById("places-list");
    if (!placesList) return;

    placesList.innerHTML = "";
    places.forEach(place => {
        const card = document.createElement("div");
        card.classList.add("place-card");

        const name = document.createElement("h3");
        name.textContent = place.name;

        const price = document.createElement("p");
        price.textContent = `$${place.price} per night`;

        const button = document.createElement("button");
        button.textContent = "View Details";
        button.addEventListener("click", () => { window.location.href = `place.html?id=${place.id}`; });

        card.appendChild(name);
        card.appendChild(price);
        card.appendChild(button);
        placesList.appendChild(card);
    });
}

function displayPlaceDetails(place) {
    const details = document.getElementById("place-details");
    if (!details) return;
    details.innerHTML = "";

    const name = document.createElement("h2");
    name.textContent = place.name;
    const description = document.createElement("p");
    description.textContent = place.description;
    const price = document.createElement("p");
    price.textContent = `Price per night: $${place.price}`;

    details.appendChild(name);
    details.appendChild(description);
    details.appendChild(price);
}

function displayReviews(reviews) {
    const reviewsList = document.getElementById("reviews-list");
    if (!reviewsList) return;
    reviewsList.innerHTML = "";

    if (reviews.length === 0) {
        const li = document.createElement("li");
        li.textContent = "No reviews yet.";
        reviewsList.appendChild(li);
        return;
    }

    reviews.forEach(review => {
        const li = document.createElement("li");
        li.textContent = `${review.user_name || 'Anonymous'} (${review.rating}/5): ${review.text}`;
        reviewsList.appendChild(li);
    });
}

// ----------- Price Filter -----------
function filterPlaces() {
    const filter = document.getElementById("price-filter");
    if (!filter) return;

    const value = filter.value;

    if (value === "all") {
        displayPlaces(allPlaces);
        return;
    }

    const maxPrice = parseInt(value, 10);

    const filtered = allPlaces.filter(place => place.price <= maxPrice);

    displayPlaces(filtered);
}

// ----------- Main -----------
document.addEventListener("DOMContentLoaded", () => {

    // LOGIN PAGE
    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", handleLogin);
        return;
    }

    // INDEX PAGE
    if (document.getElementById("places-list")) {
        fetchPlaces();

        const filter = document.getElementById("price-filter");
        if (filter) {
            filter.addEventListener("change", filterPlaces);
        }

        return;
    }

    // PLACE DETAILS PAGE
    if (document.getElementById("place-details")) {
        const token = getCookie("token");
        const placeId = getPlaceIdFromURL();
        fetchPlaceDetails(token, placeId);
    }

    // ADD REVIEW FORM
    const reviewForm = document.getElementById("review-form");
    if (reviewForm) {
        const token = checkAuthenticationRedirect();
        const placeId = getPlaceIdFromURL();

        reviewForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById("review-text").value;
            const rating = parseInt(document.getElementById("rating").value, 10);

            const success = await submitReview(token, placeId, reviewText, rating);

            if (success) {
                reviewForm.reset();

                const reviewsList = document.getElementById("reviews-list");
                if (reviewsList) {
                    const li = document.createElement("li");

                    const payload = parseJwt(token);
                    const userName = payload?.sub || "Anonymous";

                    li.textContent = `${userName} (${rating}/5): ${reviewText}`;
                    reviewsList.appendChild(li);
                }
            }
        });
    }
});
