const apiUrl = 'https://fakestoreapi.com/products';

const tableBody = document.querySelector('#productsTable tbody');
const addProductForm = document.querySelector('#addProductForm');

function renderProduct(product) {
  const tr = document.createElement('tr');
  tr.innerHTML = `
    <td>${product.id}</td>
    <td>${product.title}</td>
    <td>${product.price}</td>
    <td>${product.description}</td>
  `;
  tableBody.appendChild(tr);
}

function loadProducts() {
  fetch(apiUrl)
  .then(response => {
    if (!response.ok) {
      throw new Error("HTTP error! status: " + response.status);
    }
    return response.json();
  })
  .then(products => {
    products.slice(0,100).forEach(prod => renderProduct(prod));
  })
  .catch(error => {
    console.error("Error loading products: ", error);
  });
}

addProductForm.addEventListener('submit', event => {
  event.preventDefault();
  const formData = new FormData(addProductForm);

  const newProduct = {
    title: formData.get("title"),
    price: formData.get("price"),
    description: formData.get("description") || ""
  };

  fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type" : "application/json"
    },
    body: JSON.stringify(newProduct)
  })
  .then(response => {
    if (!response.ok) {
      throw new Error("HTTP error! status: " + response.status);
    }
    return response.json();
  })
  .then(createdProduct => {
    renderProduct(createdProduct);
  })
  .catch(error => {
    console.warn("POST failed; adding locally only. Error: ", error);
    const div = document.getElementById("errorMessage");
    div.innerHTML = `<h1>Error while inserting the new product</h1>`;
  })
  addProductForm.reset();
});

loadProducts();