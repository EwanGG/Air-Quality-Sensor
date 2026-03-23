function getData () {

    fetch("/air_data")
        .then(response => response.json())
        .then(data => {

            document.getElementById("pm25").innerText = data.pm25;
            document.getElementById("temperature").innerText = data.temperature; // FIXED
            document.getElementById("humidity").innerText = data.humidity;

        })
        .catch(error => console.error("Error:", error));
}
window.onload = getData;