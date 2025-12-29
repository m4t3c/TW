const order = {name:"Matteo", product:"", amount:0, valid:false};

function validaOrdine() {
    order.product = document.getElementById("product").value;
    order.amount =  parseInt(document.getElementById("amount").value);

    if(order.product !== "" && order.amount > 0) {
        order.valid = true;
    }

    console.log(
        "Cliente: " + order.name + " | Prodotto: " + order.product + " | Quantità: " + order.amount + " | Validità " + order.valid
    );

    if (order.valid) {
        alert("Ordine valido!");
    } else
    {
        alert("Ordine non valido!");
    }
}