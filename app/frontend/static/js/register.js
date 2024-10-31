document.getElementById('registerForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const confirm_password = document.getElementById('confirm_password').value;

    const response = await fetch('/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password, confirm_password })
    });

    const data = await response.json();
    if (response.ok) {
        alert("Registro exitoso! Redirigiendo al inicio de sesión.");
        window.location.href = "/login";
    } else {
        alert("Error: " + data.message);
    }
});
