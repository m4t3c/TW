const searchTitle = document.getElementById("searchTitle");
const post = document.querySelectorAll(".post");

searchTitle.addEventListener("input", function() {
    const input = searchTitle.value.trim().toLowerCase();
    post.forEach(function(article) {
        const title = article.querySelector("h3").textContent.trim().toLowerCase();
        if (title.includes(input)) {
            article.style.display = "block";
        } else {
            article.style.display = "none";
        }
    })
});