document.addEventListener("DOMContentLoaded", () => {
    const output = document.getElementById("output");
    const loginForm = document.getElementById("loginForm");
    const fetchUsers = document.getElementById("fetchUsers");
    const fetchUser = document.getElementById("fetchUser");

    let token = null;

    loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const response = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.status === 200) {
            token = data.token;
            output.textContent = "Logged in successfully";
        } else {
            output.textContent = "Failed to login";
        }
    });

    fetchUsers.addEventListener("click", async () => {
        const response = await fetch("/api/users", {
            headers: { Authorization: `Bearer ${token}` }
        });
        const data = await response.json();
        output.textContent = JSON.stringify(data, null, 2);
    });

    // ... (other event listeners)
});
