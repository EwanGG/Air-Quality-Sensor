document.getElementById("loginBtn").addEventListener("click", login);

async function login() {
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    try {
        const response = await fetch("/index", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (data.status === "success") {
            document.getElementById("message").innerText = "Login successful";
            window.location.href = "background_info.html";
        } else {
            document.getElementById("message").innerText = "Login failed";
        }

    } catch (error) {
        console.error("Login error:", error);
    }
}