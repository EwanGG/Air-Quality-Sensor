const socket = io("http://localhost:14473", {
    transports: ["websocket"]
});

socket.on('connect', () => {
    console.log("Connected");
});

function updateElement(id, value, statusFn) {
    const el = document.getElementById(id);

    el.innerText = value ?? "N/A";

    // Reset classes
    el.classList.remove("good", "moderate", "bad");

    if (value != null && statusFn) {
        el.classList.add(statusFn(value));
    }
}

socket.on('air_data', (data) => {
    console.log("AIR:", data);

    updateElement("gas", data.gas, getGasStatus);
    updateElement("temperature", data.temperature, getTemperatureStatus);
    updateElement("humidity", data.humidity, getHumidityStatus);
    updateElement("pressure", data.pressure, getPressureStatus);
    updateElement("iaq", data.iaq, getIAQStatus);
    updateElement("co2", data.co2, getCO2Status);
    updateElement("voc", data.voc, getVOCStatus);
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

        updateElement("gas", data.gas, getGasStatus);
        updateElement("temperature", data.temperature, getTemperatureStatus);
        updateElement("humidity", data.humidity, getHumidityStatus);
        updateElement("pressure", data.pressure, getPressureStatus);
        updateElement("iaq", data.iaq, getIAQStatus);
        updateElement("co2", data.co2, getCO2Status);
        updateElement("voc", data.voc, getVOCStatus);

        document.getElementById("lat").innerText = data.latitude ?? "N/A";
        document.getElementById("lon").innerText = data.longitude ?? "N/A";

    } catch (error) {
        console.error("Error:", error);
    }
}

const GOOD = "good";
const MODERATE = "moderate";
const BAD = "bad";

function getGasStatus(gas) {
    if (gas >= 20) return GOOD;
    if (gas >= 15) return MODERATE;
    return BAD;
}

function getPressureStatus(pressure) {
    if (pressure >= 980 && pressure <= 1030) return GOOD;
    return MODERATE; // never really "bad"
}

function getHumidityStatus(humidity) {
    if (humidity >= 40 && humidity <= 60) return GOOD;
    if ((humidity >= 30 && humidity < 40) || (humidity > 60 && humidity <= 70)) return MODERATE;
    return BAD;
}

function getTemperatureStatus(temp) {
    if (temp >= 18 && temp <= 24) return GOOD;
    if ((temp >= 15 && temp < 18) || (temp > 24 && temp <= 28)) return MODERATE;
    return BAD;
}

function getIAQStatus(iaq) {
    if (iaq <= 50) return GOOD;
    if (iaq <= 100) return MODERATE;
    return BAD;
}

function getCO2Status(co2) {
    if (co2 <= 800) return GOOD;
    if (co2 <= 1200) return MODERATE;
    return BAD;
}

function getVOCStatus(voc) {
    if (voc <= 100) return GOOD;
    if (voc <= 200) return MODERATE;
    return BAD;
}

window.onload = () => {
    getData();

    document.getElementById("refreshBtn")
        .addEventListener("click", getData);
};