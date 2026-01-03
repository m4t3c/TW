function getRadioCheckedValue(radioGroup) {
    for (option of radioGroup) {
        if (option.checked) {
            return option.values;
        }
    }
}

function getCheckboxValues(checkBox) {
    var checked = []
    for (option of checkBox) {
        if (option.checked) {
            checked.push(option.value)
        }
    }

    return checked;
}

function getSelectedValues(sel) {
    return sel.options[sel.selectedIndex].value;
}

const form = document.getElementById("regForm");

form.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent default form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = document.getElementById('email').value;
    const gender = getRadioCheckedValue(document.getElementsByName('gender'));
    const interests = getCheckboxValues(document.getElementsByName('interests'));
    const country = getCheckboxValues(document.getElementsByName('country'));

    const params = {
        username: username,
        password: password,
        email: email,
        gender: gender,
        interests: interests,
        country: country
    };

    // Use the Fetch API to make the POST request
    fetch("https://httpbin.org/post", {
        method: "POST",
        headers: {
            "Content-type": "application/json"
        },
        body: JSON.stringify(params)
    })
    // Check if HTTP status is OK (200–299)
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok: " + response.status);
        }
        return response.json();
    })

    .then(result => {
    // Assuming result.data is a JSON-string that needs parsing
    const data = JSON.parse(result.data);
    const responseUsername = data.username;
    document.getElementById("response").innerHTML = "Utente " + responseUsername + " creato!";
    document.getElementById("response").style.color = "green";
    })
    // Handle the error
    .catch(error => {
        document.getElementById("response").innerHTML = "Errore nella creazione dell'utente!";
        document.getElementById("response").style.color = "red";
        console.error("Fetch error: ", error);
    })
});

