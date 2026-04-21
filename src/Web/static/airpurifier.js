async function getData () {

    try {
        const response = await fetch('http://164.138.80.86:14473/air_data');
        const data = await response.json();

        socket.on('air_data', (data) => {
            document.getElementById("gas").innerText = data.gas;
            document.getElementById("temperature").innerText = data.temperature;
            document.getElementById("humidity").innerText = data.humidity;
            document.getElementById("pressure").innerText = data.pressure;
        });

        socket.on('gps_data', (data) => {
            document.getElementById("lat").innerText = data.latitude;
            document.getElementById("lon").innerText = data.longitude;
        });

    } catch (error) {
        console.error("Error getting data.", error);
    }
}

// Load every 5 seconds
setInterval(getData, 5000);

// Run on page load
window.onload = getData;