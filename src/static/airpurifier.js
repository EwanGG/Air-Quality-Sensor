const socket = io();

// ---------- REAL-TIME SOCKET DATA ----------
socket.on('air_data', (data) => {
    console.log("AIR:", data);

    document.getElementById("gas").innerText = data.gas ?? "N/A";
    document.getElementById("temperature").innerText = data.temperature ?? "N/A";
    document.getElementById("humidity").innerText = data.humidity ?? "N/A";
    document.getElementById("pressure").innerText = data.pressure ?? "N/A";
});

socket.on('gps_data', (data) => {
    console.log("GPS:", data);

    document.getElementById("lat").innerText = data.latitude ?? "N/A";
    document.getElementById("lon").innerText = data.longitude ?? "N/A";
});

// ---------- FALLBACK FETCH ----------
async function getData() {
    try {
        const response = await fetch("/all_data");
        const data = await response.json();

        console.log("FETCH:", data);

        document.getElementById("gas").innerText = data.gas ?? "N/A";
        document.getElementById("temperature").innerText = data.temperature ?? "N/A"; // ✅ FIXED
        document.getElementById("humidity").innerText = data.humidity ?? "N/A";
        document.getElementById("pressure").innerText = data.pressure ?? "N/A";
        document.getElementById("lat").innerText = data.latitude ?? "N/A";
        document.getElementById("lon").innerText = data.longitude ?? "N/A";

    } catch (error) {
        console.error("Error getting data:", error); // ✅ FIXED
    }
}

// Run every 5 seconds
setInterval(getData, 5000);

// Run on page load
window.onload = getData;