function getData () {

    fetch("/airdata")
        .then(response => response.json())
        .then(data => {

            document.getElementById("pm25").innerText = data.pm25;
            document.getElementById("temp").innerText = data.temprature;
            document.getElementById("humidity").innerText = data.humidity;
            document.getElementById("fan").innerText = data.fan_speed;

        });
}