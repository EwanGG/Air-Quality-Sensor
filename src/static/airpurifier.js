const socket = io();

socket.on('connect', () => {
    console.log("Connected");
});

socket.on('air_data', (data) => {
    console.log("Incoming data:", data);

    // Air data
    document.getElementById("gas").innerText = data.gas ?? "N/A";
    document.getElementById("temperature").innerText = data.temperature ?? "N/A";
    document.getElementById("humidity").innerText = data.humidity ?? "N/A";
    document.getElementById("pressure").innerText = data.pressure ?? "N/A";

    // GPS data
    document.getElementById("latitude").innerText = data.latitude ?? "N/A";
    document.getElementById("longitude").innerText = data.longitude ?? "N/A";
});

async function getData() {
    try {
        const response = await fetch("/all_data");
        const data = await response.json();

        console.log("FETCH:", data);

        document.getElementById("gas").innerText = data.gas ?? "N/A";
        document.getElementById("temperature").innerText = data.temperature ?? "N/A";
        document.getElementById("humidity").innerText = data.humidity ?? "N/A";
        document.getElementById("pressure").innerText = data.pressure ?? "N/A";

        document.getElementById("latitude").innerText = data.latitude ?? "N/A";
        document.getElementById("longitude").innerText = data.longitude ?? "N/A";

    } catch (error) {
        console.error("Error:", error);
    }
}

window.onload = () => {
    getData();

    document.getElementById("refreshBtn")
        .addEventListener("click", getData);
};