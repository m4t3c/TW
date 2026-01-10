import csv
import os.path
from idlelib.rpc import request_queue

from flask import Flask, render_template, request, jsonify, redirect, url_for

#ESERCIZIO 1
def load_videogames():
    videogames = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/videogames.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['code'] = int(row['code'])
                videogames.append(row)
            return videogames
    except FileNotFoundError:
        print(f'Error: {csv_path} not found.')
        return []
    except Exception as e:
        print(f'Error loading videogames: {e}')
        return []

def load_ratings():
    ratings = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/ratings.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['videogame_code'] = int(row['videogame_code'])
                ratings.append(row)
            return ratings
    except FileNotFoundError:
        print(f'Error: {csv_path} not found.')
        return []
    except Exception as e:
        print(f'Error loading ratings: {e}')
        return []

app = Flask(__name__)

#ESERCIZIO 2
@app.route('/index')
def index():
    videogames = load_videogames()
    ratings = load_ratings()
    videogame_avg_ratings = {}
    for videogame in videogames:
        game_ratings = [float(r['rating']) for r in ratings if r['videogame_code'] == videogame['code']]
        if game_ratings:
            videogame_avg_ratings[videogame['code']] = round(sum(game_ratings)/ len(game_ratings), 1)
        else:
            videogame_avg_ratings[videogame['code']] = None

    return render_template('index.html', videogames=videogames, gameratings=videogame_avg_ratings)

#ESERCIZIO 3
@app.route('/videogame/<game_code>')
def videogame_detail(game_code):
    videogames = load_videogames()
    ratings = load_ratings()

    videogame = next((v for v in videogames if v['code'] == int(game_code)), None)
    videogame_ratings = [r for r in ratings if r['videogame_code'] == int(game_code)]

    if not videogame:
        return "Videogioco non trovato", 404
    return render_template("game_detail.html", videogame = videogame, ratings = videogame_ratings)

#ESERCIZIO 4
@app.route('/api/add_rating', methods=['POST'])
def add_rating():
    username = request.form["username"]
    videogame_code = request.form["videogame_code"]
    rating = request.form["rating"]
    csv_path = os.path.join(os.path.dirname(__file__), 'data/ratings.csv')
    with open(csv_path, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, videogame_code, rating])

    return redirect(url_for('videogame_detail', game_code=videogame_code))

#ESERCIZIO 5
@app.route('/api/ratings', methods=['GET'])
def get_ratings():
    ratings = load_ratings()
    return jsonify(ratings)

@app.route('/api/game_ratings/<game_code>', methods=['GET'])
def get_ratings_game(game_code):
    ratings = load_ratings()
    game_ratings = [r for r in ratings if r['videogame_code']== int(game_code)]
    return jsonify(game_ratings)

#ESERCIZIO 6
@app.route('/react')
@app.route('/react/<path:react_path>')
def react(react_path=None):
    return render_template('index_react.html')

#ESERCIZIO 7
@app.route('/api/videogames', methods=['GET'])
def get_videogames():
    videogames = load_videogames()
    return jsonify(videogames)

#ESERCIZIO 8
@app.route('/api/add_videogames', methods=['POST'])
def add_videogame():
    data = request.get_json()
    name = data.get('name')
    company = data.get('company')

    videogames = load_videogames()
    new_videogame_code = str(len(videogames) + 1)

    csv_path = os.path.join(os.path.dirname(__file__), 'data/videogames.csv')
    with open(csv_path, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_videogame_code, name, company])

    return jsonify({'message': 'Video game added correctly', 'code': new_videogame_code}), 201

if __name__ == '__main__':
    app.run(debug=True)
