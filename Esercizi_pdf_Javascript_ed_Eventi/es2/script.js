const conferma = document.getElementById("conferma");
const form = document.getElementById("invioTesi");

form.addEventListener("submit", (event) => {
    event.preventDefault();
    const name = document.getElementById("name").value;
    const course = document.getElementById("course").value;
    const title = document.getElementById("title").value;

    conferma.textContent = "Grazie " + name + "! Il tuo titolo di tesi \"" + title + "\" per il corso \"" + course + "\" è stato registrato.";
})