document.addEventListener("DOMContentLoaded", () => {

    const loginForm = document.getElementById("login-form");
    if (loginForm) {
        loginForm.addEventListener("submit", handleLogin);
        return; // stop on login page
    }

    const placesList = document.getElementById("places-list");
    if (placesList) {
        fetchAndDisplayPlaces(); // index page
        return;
    }

    const placeDetails = document.getElementById("place-details");
    if (placeDetails) {
        const placeId = getPlaceIdFromURL();
        if (placeId) checkAuthentication(placeId); // place page
        return;
    }
});

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("id"); // return UUID
}

function getCookie(name) {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) return cookie.substring(name.length + 1);
    }
    return null;
}

async function handleLogin(event) {
    event.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const response = await fetch("http://localhost:5000/api/v1/auth/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email, password})
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

async function fetchAndDisplayPlaces() {
    try {
        const response = await fetch("http://localhost:5000/api/v1/places");
        if (!response.ok) throw new Error("Failed to fetch places");
        const places = await response.json();
        displayPlaces(places);
    } catch (error) {
        console.error(error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById("places-list");
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
        button.addEventListener("click", () => {
            window.location.href = `place.html?id=${place.id}`; // use UUID
        });

        card.appendChild(name);
        card.appendChild(price);
        card.appendChild(button);

        placesList.appendChild(card);
    });
}

function checkAuthentication(placeId) {
    const token = getCookie("token");
    const addReviewSection = document.getElementById("add-review");
    if (addReviewSection) addReviewSection.style.display = token ? "block" : "none";
    fetchPlaceDetails(token, placeId);
}

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) headers["Authorization"] = `Bearer ${token}`;
        const response = await fetch(`http://localhost:5000/api/v1/places/${placeId}`, {
            method: "GET",
            headers
        });
        if (!response.ok) throw new Error("Failed to fetch place details");
        const place = await response.json();
        displayPlaceDetails(place);
    } catch (error) {
        console.error(error);
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById("place-details");
    placeDetails.innerHTML = "";

    const name = document.createElement("h2");
    name.textContent = place.name;

    const description = document.createElement("p");
    description.textContent = place.description;

    const price = document.createElement("p");
    price.textContent = `Price per night: $${place.price}`;

    placeDetails.appendChild(name);
    placeDetails.appendChild(description);
    placeDetails.appendChild(price);
}
