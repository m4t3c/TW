const voti = document.getElementById("grades");
const bottone = document.querySelector("button");
const risultati = document.getElementById("results");

bottone.addEventListener("click", function () {
    let valid = true;
    const input = voti.value;
    if (input.trim() == "") {
        risultati.textContent = "Errore: non è stato passato nessun voto.";
        return;
    }

    const votiNumerici = input.split(",").map(Number);
    votiNumerici.forEach(function (voto) {
        if (isNaN(voto) || voto < 18 || voto > 30) {
            valid = false;
        }
    });

    if (!valid) {
        risultati.textContent = "Errore: voti non validi.";
        return;
    }

    const min = Math.min(...votiNumerici);
    const max = Math.max(...votiNumerici);
    const sum = votiNumerici.reduce(function(acc, voto) {
        return acc + voto;
    }, 0)
    const media = sum / votiNumerici.length;
    risultati.textContent = "Valori: " + input + " Voto minimo: " + min + " Voto massimo: " + max + " Media dei voti: " + media.toFixed(2);
})