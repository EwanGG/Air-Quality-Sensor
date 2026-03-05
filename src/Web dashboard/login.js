document.getElementById("loginBtn").addEventListener("click", login);

function login() {

    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    if(username === "raspberry" && password === "team17") {
        document.getElementById("message").innerText = "Login successful";
    }
    else {
        document.getElementById("message").innerText = "Login failed";
    }
}

/**
 * This is where Javascript sends in the request for the login
  */
fetch("/login", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "username": document.getElementById("username").value,
        "password": document.getElementById("password").value
    })
})
.then(response => response.json())
.then(data => {
    if(data.status === "success"){
        alert("Login Successful");
    }
})