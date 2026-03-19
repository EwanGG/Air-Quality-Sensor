function getData () {

    fetch("/airdata")
        .then(response => response.json())
        .then(data => {

            document.getElementById("pm25").innerText = data.pm25;
            document.getElementById("temp").innerText = data.temperature; // FIXED
            document.getElementById("humidity").innerText = data.humidity;

        })
        .catch(error => console.error("Error:", error));
}
window.onload = getData;