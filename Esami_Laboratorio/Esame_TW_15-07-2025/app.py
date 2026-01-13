from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import csv
import os
import random
from datetime import datetime

#ESERCIZIO 1
def load_questions():
    questions = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/questions.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if 'correct_answers' in row:
                    try:
                        row['correct_answers'] = eval(row['correct_answers'])
                    except:
                        row['correct_answers'] = []
                questions.append(row)
        return questions
    except FileNotFoundError:
        print(f'Warning: {csv_path} not found.')
        return []
    except Exception as e:
        print(f'Error loading questions: {e}')
        return []

def load_quizzies():
    quizzies = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/quizzies.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                quizzies.append(row)
        return quizzies
    except FileNotFoundError:
        print(f'Warning: {csv_path} not found.')
        return []
    except Exception as e:
        print(f'Error loading quizzies: {e}')
        return []

app = Flask(__name__)
app.secret_key = 'lol'
#ESERCIZIO 2
@app.route('/')
@app.route('/index')
def index():
    quizzies = load_quizzies()
    return render_template('index.html', quizzies=quizzies)

#ESERCIZIO 3
@app.route('/add_quiz', methods=['POST'])
def add_quiz():
    name = request.form.get('name')
    num_questions = int(request.form.get('num_questions'))
    questions = load_questions()

    if num_questions > len(questions):
        flash(f"Errore, Richieste {num_questions} domande ma ce ne sono massimo {questions}")
        return redirect(url_for('index'))

    selected_questions = random.sample(questions, num_questions)
    questions_code = [q['question_code'] for q in selected_questions]

    quizzies = load_quizzies()
    codes = [int(el['quiz_code'][4:]) for el in quizzies]
    if len(codes) > 0:
        quiz_code = f"QUIZ{max(codes) + 1}"
    else:
        quiz_code = "QUIZ1"

    csv_path = os.path.join(os.path.dirname(__file__), 'data/quizzies.csv')
    with open(csv_path, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([quiz_code, name, str(questions_code)])

    flash(f"Quiz: {name} creato correttamente!")
    return redirect(url_for('index'))

#ESERCIZIO 4
@app.route('/quiz/<quiz_code>')
def quiz_detail(quiz_code):
    quizzes = load_quizzies()
    quiz = next((q for q in quizzes if q['quiz_code'] == quiz_code), None)
    if quiz:
        questions = load_questions()
        quiz_questions = []
        for question in questions:
            for q in eval(quiz['question_list']):
                if question['question_code'] == q:
                    quiz_questions.append(question)
                    break

        print(quiz_questions)
        return render_template('quiz_details.html', quiz = quiz, questions = quiz_questions)
    else:
        quiz_questions = []
        return render_template('quiz_details.html', quiz=quiz, questions = quiz_questions)


#ESERCIZIO 5
@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify(load_questions())

@app.route('/api/questions/<quiz_code>', methods=['GET'])
def get_questions_quiz(quiz_code):
    quizzes = load_quizzies()
    quiz = next((q for q in quizzes if q['quiz_code'] == quiz_code), None)
    if quiz:
        quiz_questions = []
        questions = load_questions()
        for question in questions:
            for q in eval(quiz['question_list']):
                if question['question_code'] == q:
                    quiz_questions.append(question)
                    break
        return jsonify(quiz_questions)


#ESERCIZIO 6
@app.route('/react')
@app.route('/react/<path:react_path>')
def react(react_path=None):
    return render_template('index_react.html')

#ESERCIZIO 8
@app.route('/api/add_questions', methods=['POST'])
def add_questions():
    data = request.get_json()
    statement = data.get('statement')
    answer_1 = data.get('answer_1')
    answer_2 = data.get('answer_2')
    answer_3 = data.get('answer_3')
    answer_4 = data.get('answer_4')
    correct_answers = data.get('correct_answers')

    questions = load_questions()
    codes = [int(q['question_code'][1:]) for q in questions]
    if len(codes) > 0:
        question_code = f"Q{max(codes) + 1}"
    else:
        question_code = "Q1"

    csv_path = os.path.join(os.path.dirname(__file__), 'data/questions.csv')
    try:
        with open(csv_path, mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([question_code, statement, answer_1, answer_2, answer_3, answer_4, str(correct_answers)])
        return jsonify({'success': 'true', 'message': 'Domanda ' + question_code + ' creata correttamente'}), 201
    except FileNotFoundError:
        return jsonify({'success': 'false', 'message': 'File non trovato'}), 404
    except Exception as e:
        print(e)
        return jsonify({'success': 'false', 'message': 'Impossibile aggiungere la domanda ' + e})

if __name__ == '__main__':
    app.run(debug=True)
