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