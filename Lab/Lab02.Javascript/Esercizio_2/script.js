const arr = [
    {
        url: "https://www.armandoalpantheon.it/wp-content/uploads/2023/03/Primavera-a-Roma-%E2%80%93-Il-Colosseo-e-gli-scavi-di-Ostia-Antica-armando-al-pantheon-768x480.jpg",
        title: "Colosseo",
        description: "Originariamente conosciuto come Anfiteatro Flavio è il più grande anfiteatro romano del mondo.",
    },
    {
        url: "https://www.donne.it/wp-content/uploads/2023/10/intelligenza-artificiale-768x512.jpg",
        title: "Intelligenza Artificiale",
        description: "Nel suo significato più ampio, è la capacità di un sistema artificiale di simulare l'intelligenza umana attraverso l'ottimizzazione di funzioni matematiche.",
    },
    {
        url: "https://png.pngtree.com/background/20230525/original/pngtree-floral-wallpaper-with-brown-and-brown-paint-picture-image_2735082.jpg",
        title: "Linguaggio dei fiori",
        description: "Modo di comunicazione ottocentesco per cui i fiori e gli allestimenti floreali venivano utilizzati per esprimere sensazioni che non sempre potevano essere pronunciate.",
    }
];


function createCard(data) {
    // div representing a card
    var card = document.createElement("div");
    card.className = "bg-white rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow";

    // Create the image element
    var image = document.createElement("img");
    image.src = data.url;
    image.className = "w-full h-48 object-cover";

    // Append the image to Card div
    card.appendChild(image);

    // Div for the title and the paragraph (textcontainer)
    var textContainer = document.createElement("div");
    textContainer.className = "p-6 text-center";

    // Create the title element
    var title = document.createElement("h3");
    title.className = "font-semibold text-gray-800 text-xl mb-3";
    title.appendChild(document.createTextNode(data.title));
    // Append the title to the textcontainer div
    textContainer.appendChild(title);

    // Create the description element
    var description = document.createElement("p");
    description.className = "text-gray-600 leading-relaxed";
    description.appendChild(document.createTextNode(data.description));

    // Append the paragraph to the textcontainer div
    textContainer.appendChild(description);

    // Append the textcontainer to the Card div
    card.appendChild(textContainer);

    // Append the created card to the container
    document.getElementById("container").appendChild(card);
    
}
