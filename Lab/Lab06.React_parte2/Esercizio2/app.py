import os
import csv
from flask import Flask, render_template, jsonify


app = Flask(__name__)


def load_products():
    products = []
    with open('data/products.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            products.append(row)
    return products

@app.route('/products')
def index_react():
    return render_template('index_react.html')


@app.route('/api/products', methods=['GET'])
def get_all_products():
    return jsonify(load_products())


@app.route('/api/products/<product_code>', methods=['GET'])
def get_products_details(product_code):
    products = load_products()
    for product in products:
        if product['product_code'] == product_code:
            print(product)
            return jsonify(product)

    return jsonify({'success': False, 'message': 'Prodotto non trovato!'}), 404


if __name__ == '__main__':
    app.run(debug=True)
