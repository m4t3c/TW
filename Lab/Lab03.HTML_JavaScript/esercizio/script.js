const form = document.querySelector("form");

form.addEventListener("submit", function (event) {
    let valid = true;
    const username = document.getElementById("username");
    const usernameError = username.nextSibling;
    usernameError.textContent = "";
    if (username.value.trim() === "") {
        usernameError.textContent = "Username non valido";
        valid = false;
    }
    
    const email = document.getElementById("email");
    const emailError = email.nextSibling;
    emailError.textContent = "";
    if (!email.value.trim().endsWith("gmail.com") && !email.value.trim().endsWith("yahoo.it")) {
        emailError.textContent = "Email non valida";
        valid = false;
    }

    const phone = document.getElementById("phone");
    const phoneError = phone.nextSibling;
    phoneError.textContent = "";
    if (isNaN(phone.value) || phone.value.trim().length !== 10) {
        phoneError.textContent = "Numero non valido";
        valid = false;
    } 

    const password1 = document.getElementById("password1");
    const password2 = document.getElementById("password2");
    const passwordError1 = password1.nextSibling;
    passwordError1.textContent = "";
    if (password1.value.trim().length < 8) {
        passwordError1.textContent = "La password deve contenere almeno 8 caratteri";
        valid = false;        
    }

    const passwordError2 = password2.nextSibling;
    passwordError2.textContent = "";
    if (password1.value !== password2.value) {
        passwordError2.textContent = "Le due password non corrispondono";
        valid = false;
    }

    if (!valid) {
        event.preventDefault;
    }
})