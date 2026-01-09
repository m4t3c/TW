from flask import Flask, render_template, jsonify, request
import csv
import os

app = Flask(__name__)

#ESERCIZIO 1
def load_products():
    products = []
    csv_path = os.path.join(os.path.dirname(__file__),'data/products.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8')as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                products.append(row)
        return products
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found.")
        return []
    except Exception as e:
        print(f"Error loading product: {e}")
        return []

@app.route('/products')
def products():
    products = load_products()
    return jsonify(products)

#ESERCIZIO 2
@app.route('/index')
def index():
    products = load_products()
    return render_template('index.html', products=products)

#ESERCIZIO 3
@app.route('/product/<product_code>')
def product_detail(product_code):
    products = load_products()
    product = next((p for p in products if p['codice_prodotto'] == product_code), None)
    if product:
        return render_template('product_detail.html', product=product)
    else:
        return "Prodotto non trovato", 404

#ESERCIZIO 4
@app.route('/api/buy/<product_code>', methods=['POST'])
def buy_product(product_code):
    products = load_products()
    for product in products:
        if product['codice_prodotto'] == product_code:
            if int(product['disponibilita']) > 0:
                product['disponibilita'] = str(int(product['disponibilita']) - 1)
                file_path = os.path.join(os.path.dirname(__file__), 'data/products.csv')
                with open(file_path, mode='w', encoding='utf-8', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=product.keys())
                    writer.writeheader()
                    writer.writerows(products)
                return jsonify({'message': 'Prodotto acquistato con successo', 'disponibilita': int(product['disponibilita'])})
            else:
                return jsonify({'error': 'Prodotto non disponibile'}), 400
    return jsonify({'error': 'Prodotto non disponibile'}), 404

#ESERCIZIO 5a
@app.route('/api/products', methods=['GET'])
def def_products():
    products = load_products()
    return jsonify(products)

#ESERCIZIO 5b
@app.route('/api/product/<product_code>', methods=['GET'])
def get_product(product_code):
    products = load_products()
    product = next((p for p in products if p['codice_prodotto'] == product_code), None)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Prodotto non trovato'}), 404

#ESERCIZIO 6
@app.route('/react')
def home():
    return render_template('index_react.html')

if __name__ == '__main__':
    app.run(debug=True)
