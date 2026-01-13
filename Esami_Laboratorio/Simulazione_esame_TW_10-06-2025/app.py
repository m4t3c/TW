import csv
import os

from flask import Flask, render_template, request, jsonify, redirect, url_for

#ESERCIZIO 1
def load_library():
    library = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/library.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                library.append(row)
            return library
    except FileNotFoundError:
        print(f"File {csv_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {csv_path}: {e}")
        return []

def load_reviews():
    reviews = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/reviews.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                reviews.append(row)
            return reviews
    except FileNotFoundError:
        print(f"File {csv_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {csv_path}: {e}")
        return []

app = Flask(__name__)

#ESERCIZIO 2
@app.route('/')
def books():
    books = load_library()
    return render_template('index.html', books=books)

#ESERCIZIO 3
@app.route('/libro/<codice_libro>')
def book_detail(codice_libro):
    books = load_library()
    book = next((book for book in books if book['code'] == codice_libro), None)
    return render_template('book_details.html', book=book)

#ESERCIZIO 4
@app.route('/api/reviews', methods=['POST'])
def reviews():
    data = request.get_json()
    new_review = {
        'username': data['username'],
        'book_code': data['book_code'],
        'text': data['text']
    }
    reviews = load_reviews()
    codes = [int(r['code'][1:]) for r in reviews]
    if len(codes) > 0:
        code_with_zeros = str(max(codes) + 1)
        code_with_zeros.zfill(3)
        print(code_with_zeros)
        review_code = f'R{code_with_zeros}'
    else:
        review_code = 'R001'

    new_review['code'] = review_code
    csv_path = os.path.join(os.path.dirname(__file__), 'data/reviews.csv')
    try:
        with open(csv_path, mode='a', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['code', 'username', 'book_code', 'text'])
            writer.writerow(new_review)
        return jsonify({'success': 'true', 'message': 'Review added successfully!'}), 201
    except FileNotFoundError:
        return jsonify({'success': 'false', 'message': 'File not found!'}), 404
    except Exception as e:
        return jsonify({'success': 'false', 'message': f'Error adding review: {e}'}), 500

#ESERCIZIO 5
@app.route('/api/books', methods=['GET'])
def api_books():
    books = load_library()
    return jsonify(books)

@app.route('/api/reviews/<code>', methods=['GET'])
def api_book_get_review(code):
    books = load_library()
    book = next((book for book in books if book['code'] == code), None)
    if book:
        reviews = load_reviews()
        book_reviews = [r for r in reviews if r['book_code'] == code]
        return jsonify(book_reviews)
    else:
        return jsonify({'message': 'Book not found'}), 404

#ESERCIZIO 6
@app.route('/react')
@app.route('/react/<path:path_react>')
def react(path_react=None):
    return render_template('index_react.html')

@app.route('/api/books', methods=['GET'])
def api_books_react():
    books = load_library()
    return jsonify(books)

@app.route('/api/add_book', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    year = data.get('year')
    genre = data.get('genre')

    books = load_library()
    codes = [int(b['code'][2:]) for b in books]
    if len(codes) > 0:
        code_num = str(max(codes) + 1)
        code_with_zeros = code_num.zfill(3)
        code = f'LB{code_with_zeros}'
    else:
        code = "LB001"

    new_book = {'code': code, 'title': title, 'author': author, 'year': year, 'genre': genre}
    csv_path = os.path.join(os.path.dirname(__file__), 'data/library.csv')
    try:
        with open(csv_path, mode='a', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['code', 'title', 'author', 'year', 'genre'])
            writer.writerow(new_book)
        return jsonify({'success': 'true', 'message': 'Book added successfully!'}), 201
    except FileNotFoundError:
        return jsonify({'success': 'false', 'message': 'File not found!'}), 404
    except Exception as e:
        return jsonify({'success': 'false', 'message': f'Error adding book: {e}'}), 500

#ESERCIZIO 7
@app.route('/api/book/<book_code>', methods=['GET'])
def get_book(book_code):
    books = load_library()
    book = next((book for book in books if book['code'] == book_code), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({'message': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
