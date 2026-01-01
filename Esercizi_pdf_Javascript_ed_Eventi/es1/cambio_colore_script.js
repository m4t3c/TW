const redButton = document.getElementById("red");
const greenButton = document.getElementById("green");
const blueButton = document.getElementById("blue");
const resetButton = document.getElementById("reset");

redButton.addEventListener("click", function() {
    document.body.style.backgroundColor = "red";
})

greenButton.addEventListener("click", function() {
    document.body.style.backgroundColor = "green";
})

blueButton.addEventListener("click", function() {
    document.body.style.backgroundColor = "blue";
})

resetButton.addEventListener("click", function() {
    document.body.style.backgroundColor = "white";
})