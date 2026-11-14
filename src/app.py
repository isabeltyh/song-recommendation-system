"""
Flask web interface for the Song Recommendation System.
"""
import os
import random
from flask import Flask, render_template, request, jsonify
from song_recommender import SongRecommender

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))
app.secret_key = 'song_recommender_secret'

recommender = SongRecommender()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/genres', methods=['GET'])
def get_genres():
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


@app.route('/api/discover', methods=['GET'])
def discover_songs():
    """Returns 30 random songs for the discovery feed."""
    if not recommender.songs:
        return jsonify({"success": False, "error": "No songs loaded"}), 500
        
    count = min(30, len(recommender.songs))
    random_songs = random.sample(recommender.songs, count)
    
    return jsonify({"success": True, "results": random_songs})


@app.route('/api/search_artist', methods=['GET'])
def search_artist():
    """Returns a list of songs by a specific artist."""
    artist_query = request.args.get('artist', '').strip().lower()
    if not artist_query:
        return jsonify({"success": False, "results": [], "error": "No artist provided"}), 400
        
    matches = [s for s in recommender.songs if artist_query in s["artist"].lower()]
    matches = matches[:50]  # Limit to 50 results
    
    return jsonify({"success": True, "results": matches})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)