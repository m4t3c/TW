function gestisciFrase() {
    var frase = document.getElementById("frase").value;
    var parole = frase.split(" ");

    mostraElenco(parole, "originali");

    var paroleMaiuscole = parole.map(function(parola) {
        return parola.toUpperCase();
    })

    mostraElenco(paroleMaiuscole, "maiuscole");
}

function mostraElenco(array, idContenitore) {
    var box = document.getElementById(idContenitore);
    box.innerHTML = "";

    var ul = document.createElement("ul");

    array.forEach(function(parola) {
        var li = document.createElement("li");
        li.textContent = parola;
        ul.appendChild(li);
    });

    box.appendChild(ul);

}