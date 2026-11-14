"""
Flask web interface for the Song Recommendation System.
"""
import os
from flask import Flask, render_template, request, jsonify
from song_recommender import SongRecommender

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))
app.secret_key = 'song_recommender_secret'

recommender = SongRecommender()

# ... rest of the code ...
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/genres', methods=['GET'])
def get_genres():
    # Instead of returning 5000 artist names, return just "All" 
    # (Since your dataset currently uses artist names as genres)
    return jsonify(["All Genres"])


@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.json or {}
    song_title = data.get('song_title', '')
    genre = data.get('genre', 'all')
    try:
        count = int(data.get('count', 5))
    except (TypeError, ValueError):
        return jsonify({
            "success": False,
            "error": "Recommendation count must be a positive whole number.",
            "results": [], "note": None
        }), 400

    result = recommender.recommend(song_title, genre, count)
    status = 200 if result["success"] else 400
    return jsonify(result), status


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)