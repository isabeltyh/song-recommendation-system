# Song Recommendation System

**Group 2 | DCS2114 Intelligent Systems**
- Isabel Tan Yu Huey (J25044857)
- Dabria Marie Richard (J26046015)

## Starter Source
This project is adapted from the Study Resource Recommender starter code provided by the lecturer:
https://drive.google.com/drive/folders/1mHXcUlBD_nMfj6735Pg3iTcRNViJaENy

The starter system was a rule-based recommender for study resources. Our group transformed it into a song recommendation system by replacing the dataset, rewriting the scoring engine, and building a full web application with user accounts, search, and likes.

## Live Website
https://song-recommendation-system-ihrv.onrender.com

*Note: The free Render tier may take 30-60 seconds to wake up after inactivity.*

## Presentation & Demonstration
- **Presentation Slides:** https://canva.link/fe4uc668y8y8z7g
- **Backup Demo Video:** https://drive.google.com/file/d/1rvVRbpiLuZRA2o_JCuUvjUvWg5bxeQqn/view?usp=sharing

## Running Locally
1. Install Python 3.11+
2. Install dependencies: `pip install -r requirements.txt`
3. Run the web app: `python src/app.py`
4. Open http://localhost:5000

## Project Structure
- `src/song_recommender.py` — Recommendation engine (70/30 scoring)
- `src/app.py` — Flask web server
- `src/database.py` — SQLite user database
- `data/songs.json` — 86,000+ songs crawled from Deezer API
- `templates/index.html` — Frontend
- `static/style.css` — Stylesheet

## Dataset
Built via Deezer API crawler (`crawl_deezer_albums.py`). Genre labels resolved via manual mapping (`fix_genres.py`).