function validaOrdine() {

    var uname = document.getElementById("uname").value;
    var amount = parseInt(document.getElementById("amount").value);
    var valid = false;

    if(amount > 0) {
        valid = true;
    }

    console.log(
        "Cliente: " + uname + " | Quantità: " + amount + " | Validità: " + valid
    );

    if (valid) {
        alert("Ordine confermato per: " + uname);
    } else
    {
        alert("Ordine non valido!");
    }
}