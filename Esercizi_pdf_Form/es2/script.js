function validateForm(event) {
    let valid = true;

    // recupero input
    const nameInput = document.getElementById("name");
    const emailInput = document.getElementById("email");
    const ageInput = document.getElementById("age");

    // recupero o creo span
    const nameError = getErrorSpan(nameInput);
    const emailError = getErrorSpan(emailInput);
    const ageError = getErrorSpan(ageInput);

    nameError.textContent = "";
    emailError.textContent = "";
    ageError.textContent = "";

    if (nameInput.value.trim().length < 2) {
        nameError.textContent = "Il nome deve contenere almeno 2 caratteri.";
        valid = false;        
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(emailInput.value.trim())) {
        emailError.textContent = "Inserisci un'email valida"
        valid = false;
    }

    const age = parseInt(ageInput.value, 10);
    if (isNaN(age) || age < 0 || age > 120) {
        ageError.textContent = "L'età deve essere compresa tra 0 e 120.";
        valid = false;
    }

    if(valid) {
        alert("Form inviato con successo!");
        event.target.reset();
    } else {
        event.preventDefault();
    }
}

function getErrorSpan(input) {
  let span = input.nextElementSibling;

  if (!span || span.tagName !== "SPAN") {
    span = document.createElement("span");
    span.style.color = "red";
    span.style.marginLeft = "8px";
    input.after(span);
  }

  return span;
}