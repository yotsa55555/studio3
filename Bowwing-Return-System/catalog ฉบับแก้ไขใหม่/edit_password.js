

function goBack() {
    window.history.back(); 
}

function submitChangePassword() {
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const statusMessage = document.getElementById("statusMessage");

    if (newPassword !== confirmPassword) {
        statusMessage.textContent = "Password don't match!";
        return;
    }

    fetch("/change-password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ newPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            statusMessage.style.color = "green";
            statusMessage.textContent = "Password Reset Complete.Your password has been reset successfully. You can now login with your new password.";
        } else {
            statusMessage.textContent = "Error occurred while changing the password.";
        }
    })
    .catch(error => {
        statusMessage.textContent = "Connection failed.";
        console.error("Error:", error);
    });
}

