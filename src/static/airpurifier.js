const socket = io("http://localhost:14473", {
    transports: ["websocket"]
});

socket.on('connect', () => {
    console.log("Connected");
});

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

async function getData() {
    try {
        const response = await fetch("/all_data");
        const data = await response.json();

        console.log("FETCH:", data);

        document.getElementById("gas").innerText = data.gas ?? "N/A";
        document.getElementById("temperature").innerText = data.temperature ?? "N/A";
        document.getElementById("humidity").innerText = data.humidity ?? "N/A";
        document.getElementById("pressure").innerText = data.pressure ?? "N/A";
        document.getElementById("lat").innerText = data.latitude ?? "N/A";
        document.getElementById("lon").innerText = data.longitude ?? "N/A";

    } catch (error) {
        console.error("Error:", error);
    }
}

window.onload = () => {
    getData();

    document.getElementById("refreshBtn")
        .addEventListener("click", getData);
};