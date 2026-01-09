from os import write

from flask import Flask, render_template, jsonify, request, message_flashed
import csv
import os

#ESERCIZIO 1
def load_events():
    events = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/events.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                events.append(row)
        return events
    except FileNotFoundError:
        print(f'Warning: file {csv_path} not found')
        return []
    except Exception as e:
        print(f'Error loading events: {e}')
        return []

def write_events(events):
    csv_path = os.path.join(os.path.dirname(__file__), 'data/events.csv')
    with open(csv_path, mode='w', encoding='utf-8', newline='') as csvfile:
        fieldsname = ['code', 'name', 'sport', 'date', 'place', 'available_places']
        writer = csv.DictWriter(csvfile, fieldnames=fieldsname)
        writer.writeheader()
        writer.writerows(events)


app = Flask(__name__)

#ESERCIZIO 2
@app.route('/index')
def index():
    events = load_events()
    return render_template('index.html', events=events)

#ESERCIZIO 3
@app.route('/event/<event_code>')
def event_details(event_code):
    events = load_events()
    event = next((e for e in events if e['code'] == event_code), None)
    if event:
        return render_template('event_details.html', event=event)
    return "Error: Event not found", 404

#ESERCIZIO 4
@app.route('/api/book/<event_code>', methods=['POST'])
def book(event_code):
    events = load_events()
    for event in events:
        if event['code'] == event_code:
            if int(event['available_places']) > 0:
                event['available_places'] = str(int(event['available_places']) - 1)
                write_events(events)
                return jsonify({'success': True, 'message': 'Posto prenotato con successo', 'posti_disponibili': event['available_places']})
            return jsonify({'success': False, 'error': 'Posti esauriti', 'posti_disponibili': event['available_places']}), 400
    return jsonify({'success': False, 'error': 'Evento non trovato'}), 404

#ESERCIZIO 5
@app.route('/api/events', methods=['GET'])
def api_events():
    events = load_events()
    return jsonify(events)

@app.route('/api/events/<event_code>', methods=['GET'])
def get_event(event_code):
    events = load_events()
    event = next((e for e in events if e['code'] == event_code), None)
    if event:
        return jsonify(event)
    else:
        return jsonify({'error': 'Evento non trovato'}), 404

#ESERCIZIO 6
@app.route('/react')
def react():
    return render_template('index_react.html')

if __name__ == '__main__':
    app.run(debug=True)
