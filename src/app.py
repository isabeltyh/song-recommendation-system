"""
Flask web interface for the Song Recommendation System.
"""
import os
import random
import sqlite3
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from song_recommender import SongRecommender
from database import get_db, init_db

app = Flask(__name__, 
            template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'templates'),
            static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'static'))
app.secret_key = 'super_secret_music_key' # Change this in production

recommender = SongRecommender()

@app.route('/')
def index():
    return render_template('index.html')

# --- AUTHENTICATION ---

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"success": False, "error": "Username and password required"}), 400
        
    conn = get_db()
    try:
        hashed_pw = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pw))
        conn.commit()
        return jsonify({"success": True})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "error": "Username already exists"}), 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        return jsonify({"success": True, "username": user['username']})
    
    return jsonify({"success": False, "error": "Invalid username or password"}), 401

@app.route('/api/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    username = data.get('username')
    new_password = data.get('new_password')
    
    if not username or not new_password:
        return jsonify({"success": False, "error": "Username and new password required"}), 400
        
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if not user:
        conn.close()
        return jsonify({"success": False, "error": "User not found"}), 404
        
    # Hash the new password and update it
    hashed_pw = generate_password_hash(new_password)
    conn.execute('UPDATE users SET password = ? WHERE id = ?', (hashed_pw, user['id']))
    conn.commit()
    conn.close()
    
    return jsonify({"success": True, "message": "Password updated successfully"})

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

@app.route('/api/check_auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({"logged_in": True, "username": session['username']})
    return jsonify({"logged_in": False})

# --- LIKED SONGS ---

@app.route('/api/like', methods=['POST'])
def like_song():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Must be logged in"}), 401
        
    data = request.json
    title = data.get('title')
    artist = data.get('artist')
    
    conn = get_db()
    existing = conn.execute('SELECT id FROM liked_songs WHERE user_id = ? AND song_title = ? AND song_artist = ?', 
                            (session['user_id'], title, artist)).fetchone()
    
    if existing:
        conn.execute('DELETE FROM liked_songs WHERE id = ?', (existing['id'],))
        action = "unliked"
    else:
        conn.execute('INSERT INTO liked_songs (user_id, song_title, song_artist) VALUES (?, ?, ?)', 
                     (session['user_id'], title, artist))
        action = "liked"
        
    conn.commit()
    conn.close()
    return jsonify({"success": True, "action": action})

@app.route('/api/my_likes', methods=['GET'])
def my_likes():
    if 'user_id' not in session:
        return jsonify({"success": False, "error": "Must be logged in"}), 401
        
    conn = get_db()
    likes = conn.execute('SELECT song_title as title, song_artist as artist FROM liked_songs WHERE user_id = ?', 
                         (session['user_id'],)).fetchall()
    conn.close()
    
    return jsonify({"success": True, "likes": [dict(row) for row in likes]})

# --- MUSIC ROUTES ---

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
        return jsonify({"success": False, "error": "Invalid count", "results": [], "note": None}), 400

    result = recommender.recommend(song_title, genre, count)
    status = 200 if result["success"] else 400
    return jsonify(result), status

@app.route('/api/discover', methods=['GET'])
def discover_songs():
    if not recommender.songs:
        return jsonify({"success": False, "error": "No songs loaded"}), 500
    count = min(30, len(recommender.songs))
    random_songs = random.sample(recommender.songs, count)
    return jsonify({"success": True, "results": random_songs})

@app.route('/api/search_artist', methods=['GET'])
def search_artist():
    artist_query = request.args.get('artist', '').strip().lower()
    if not artist_query:
        return jsonify({"success": False, "results": []}), 400
    # Removed the [:50] limit here
    matches = [s for s in recommender.songs if artist_query in s["artist"].lower()]
    return jsonify({"success": True, "results": matches})

@app.route('/api/search_album', methods=['GET'])
def search_album():
    album_query = request.args.get('album', '').strip().lower()
    if not album_query:
        return jsonify({"success": False, "results": []}), 400
    # Removed the [:50] limit here
    matches = [s for s in recommender.songs if album_query in s.get("genre", "").lower()]
    return jsonify({"success": True, "results": matches})

@app.route('/api/search_genre', methods=['GET'])
def search_genre():
    genre_query = request.args.get('genre', '').strip().lower()
    if not genre_query:
        return jsonify({"success": False, "results": []}), 400
    matches = [s for s in recommender.songs if s.get("genre", "").lower() == genre_query]
    if not matches:
        matches = [s for s in recommender.songs if genre_query in s.get("genre", "").lower()]
    # Removed the [:50] limit here
    return jsonify({"success": True, "results": matches})

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)