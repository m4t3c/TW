var button = document.getElementById('button');

button.onclick = function () {
    // 1. Make a GET request using Fetch API
    fetch("https://jsonplaceholder.typicode.com/posts")
        // 2. Use a promise to convert it to JSON fileConvert the response to JSON
        .then(response => {
            if (!response.ok) {
                throw new Error("Errore nella richiesta: " + response.statusText);
            }
            return response.json();
        })
        // 3. Use a promise to create HTML for each post
        .then(posts => {
            // 3.a Select the post container from the DOM            
            const postsContainer = document.getElementById("postsContainer");
            postsContainer.innerHTML = "";
            // 3.b Iterate over the posts and create HTML elements
            posts.forEach(post => {
                var postDiv = document.createElement("div");
                postDiv.className = "post";

                var postHTML = `<h3>Post ${post.id}: ${post.title}</h3><p>${post.body}</p>`;
                postDiv.innerHTML = postHTML;
                postsContainer.appendChild(postDiv);
            });
        })
        // 4. Use a promise to handle any errors``
        .catch(error => {
            console.log("Errore Fetch: " + error);
        });
};