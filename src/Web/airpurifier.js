async function getData () {

    try {
        const response = await fetch('http://164.138.80.86:14473/air_data');
        const data = await response.json();

        document.getElementById("gas").innerText = data.gas;
        document.getElementById("temperature").innerText = data.temperature;
        document.getElementById("humidity").innerText = data.humidity;
        document.getElementById("pressure").innerText = data.pressure;
        document.getElementById("lat").innerText = data.latitude;
        document.getElementById("lon").innerText = data.longitude;

        if (data.gas > 100000)
            document.getElementById("gas").style.color = "red";
        if (data.temperature > 30)
            document.getElementById("temperature").style.color = "red";
        if (data.humidity > 60)
            document.getElementById("humidity").style.color = "red";
        if (data.pressure > 1050)
            document.getElementById("pressure").style.color = "red";

    } catch (error) {
        console.error("Error getting data.", error);
    }
}

// Load every 5 seconds
setInterval(getData, 5000);

// Run on page load
window.onload = getData;