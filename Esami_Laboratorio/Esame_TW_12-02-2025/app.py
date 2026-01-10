import csv
import os.path

from flask import Flask, render_template, request, jsonify, redirect, url_for

#ESERCIZIO 1
def load_video():
    videos = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/video.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                videos.append(row)
            return videos
    except FileNotFoundError:
        print(f"Warning: {csv_path} not found.")
        return []
    except Exception as e:
        print(f"Error loading video: {e}")
        return []

def load_comments():
    comments = []
    csv_path = os.path.join(os.path.dirname(__file__), 'data/comments.csv')
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                comments.append(row)
            return comments
    except FileNotFoundError:
        print(f'Warning: {csv_path} not found.')
        return []
    except Exception as e:
        print(f"Error loading comment: {e}")
        return []
app = Flask(__name__)

#ESERCIZIO 2
@app.route('/index')
def index():
    videos = load_video()
    comments = load_comments()
    video_comment_count = {}
    for video in videos:
        video_comment_count[video['video_code']] = sum(1 for c in comments if c['video_code'] == video['video_code'])
    return render_template('index.html', videos=videos, video_comment_count=video_comment_count)

#ESERCIZIO 3
@app.route('/video/<video_code>')
def video_detail(video_code):
    videos = load_video()
    comments = load_comments()
    video = next((v for v in videos if v['video_code'] == video_code), None)
    video_comments = [c['comment'] for c in comments if c['video_code'] == video_code]

    if not video:
        return "Video not found", 404

    return render_template('video_detail.html', video=video, comments=video_comments)

#ESERCIZIO 4
@app.route('/add_comment', methods=['POST'])
def add_comment():
    video_code = request.form['video_code']
    comment = request.form['comment']
    with open('data/comments.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([video_code, comment])
    return redirect(url_for('video_detail', video_code=video_code))

#ESERCIZIO 5
@app.route('/api/comments', methods=['GET'])
def get_comments():
    comments = load_comments()
    return jsonify(comments)

@app.route('/api/comments/<video_code>', methods=['GET'])
def get_comments_video(video_code):
    comments = load_comments()
    video_comments = [c for c in comments if c['video_code'] == video_code]
    return jsonify(video_comments)

#ESERCIZIO 6
@app.route('/react')
@app.route('/react/<path:react_path>')
def react(react_path=None):
    return render_template('index_react.html')

#ESERCIZIO 7
@app.route('/api/videos', methods=['GET'])
def get_videos():
    return jsonify(load_video())

#ESERCIZIO 8
@app.route('/api/upload_video', methods=['POST'])
def upload_video():
    data = request.get_json()
    video_name = data.get('video_name')
    video_link = data.get('video_link')

    videos = load_video()
    new_video_code = str(len(videos) + 1)

    csv_path = os.path.join(os.path.dirname(__file__), 'data/video.csv')
    with open(csv_path, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_video_code, video_name, video_link])

    return jsonify({'message': 'Video added correctly', 'video_code': new_video_code}), 201

if __name__ == '__main__':
    app.run(debug=True)
