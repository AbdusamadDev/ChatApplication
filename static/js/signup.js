document.addEventListener('DOMContentLoaded', function () {
    document.getElementById("userForm").addEventListener("submit", async function (event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);
        const data = {
            username: formData.get('username'),
            email: formData.get('email'),
            password: formData.get('password')
        };

        try {
            const response = await fetch('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                const errorMessage = await response.text();
                throw new Error(errorMessage);
            }
            const responseData = await response.json();
            console.log(responseData);
            // Handle response as needed, for example, show a success message to the user
            alert("User created successfully!");
            // You can redirect the user to another page or perform any other action here
        } catch (error) {
            console.error('Error:', error);
            // Handle errors, for example, show an error message to the user
            alert("Error occurred: " + error.message);
        }
    });
})