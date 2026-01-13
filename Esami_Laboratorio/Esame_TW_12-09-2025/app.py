from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import csv
import os
import random
from datetime import datetime

#ESERCIZIO 1
def load_places():
    csv_path = os.path.join(os.path.dirname(__file__), 'data/places.csv')
    places = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                row['price'] = float(row['price'])
                places.append(row)
        return places
    except FileNotFoundError:
        print(f"File {csv_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {csv_path}: {str(e)}")
        return []

def load_itineraries():
    csv_path = os.path.join(os.path.dirname(__file__), 'data/itineraries.csv')
    itineraries = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                row['place_list'] = eval(row['place_list'])
                itineraries.append(row)
        return itineraries
    except FileNotFoundError:
        print(f"File {csv_path} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {csv_path}: {str(e)}")
        return []


app = Flask(__name__)

#ESERCIZIO 2
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', places=load_places())

#ESERCIZIO 3
@app.route('/place/<place_id>')
def place_detail(place_id):
    places = load_places()
    itineraries = load_itineraries()
    place = next((p for p in places if p['place_id'] == place_id), None)
    count_itineraries = 0
    for itinerary in itineraries:
        for p_id in (itinerary['place_list']):
            if p_id == int(place_id):
                count_itineraries += 1
    return render_template('place_detail.html', place=place, count_itineraries=count_itineraries)

#ESERCIZIO 4
@app.route('/add_place')
def add_place():
    return render_template('add_place.html')

@app.route('/api/add_place', methods=['POST'])
def add_place_api():
    data = request.get_json()
    new_place = {
        'name': data['name'],
        'category': data['category'],
        'municipality': data['municipality'],
        'image_link': data['image_link'],
        'price': data['price']
    }
    places = load_places()
    new_place_id = max([int(p['place_id']) for p in places]) + 1
    new_place['place_id'] = new_place_id

    csv_path = os.path.join(os.path.dirname(__file__), 'data/places.csv')
    try:
        with open(csv_path, mode='a', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['place_id', 'name', 'category', 'municipality', 'image_link', 'price'])
            writer.writerow(new_place)
        return jsonify({'success': True, 'message': 'Place added successfully!'}), 201
    except FileNotFoundError:
        return jsonify({'success': False, 'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error adding place: {str(e)}'}), 500

#ESERCIZIO 5
@app.route('/api/itineraries', methods=['GET'])
def itineraries_api():
    itineraries = load_itineraries()
    return jsonify(itineraries)

@app.route('/api/itineraries/<itinerary_id>', methods=['GET'])
def places_api(itinerary_id):
    itineraries = load_itineraries()
    itinerary = next((i for i in itineraries if i['itinerary_id'] == itinerary_id), None)
    if itinerary:
        places = load_places()
        place_itineraries = [p for p in places if int(p['place_id']) in itinerary['place_list']]
        return jsonify({'places': place_itineraries})
    else:
        return jsonify({'error': 'Itinerary not found'}), 404

#ESERCIZIO 6
@app.route('/react')
@app.route('/react/<path:path_react>')
def react(path_react=None):
    return render_template('index_react.html')

#ESERCIZIO 7
@app.route('/api/places')
def react_places_api():
    places = load_places()
    return jsonify(places)

#ESERCIZIO 8
@app.route('/api/add_itineraries', methods=['POST'])
def react_itineraries_api():
    data = request.get_json()
    name = data.get('name')
    duration = data.get('duration')
    place_list = data.get('place_list')

    itineraries = load_itineraries()
    new_itinerary_id = max([int(i['itinerary_id']) for i in itineraries]) + 1
    new_itinerary = {'itinerary_id': new_itinerary_id, 'name': name, 'duration': duration, 'place_list': place_list}
    csv_path = os.path.join(os.path.dirname(__file__), 'data/itineraries.csv')
    try:
        with open(csv_path, mode='a', encoding='utf-8', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['itinerary_id', 'name', 'duration', 'place_list'])
            writer.writerow(new_itinerary)
        return jsonify({'success': 'true', 'message': 'Itinerario aggiunto correttamente!'}), 201
    except FileNotFoundError:
        return jsonify({'success': 'false', 'message': 'File not found'}), 404
    except Exception as e:
        return jsonify({'success': 'false', 'message': f'Error adding itinerary: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
