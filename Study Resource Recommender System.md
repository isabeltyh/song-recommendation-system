# Study Resource Recommender System

A beginner-friendly, rule-based recommendation system designed for students. This project allows you to get personalized study resource recommendations, track your learning history, and easily modify the recommendation logic without complex coding.

## Features

- **Rule-Based Engine**: Recommends resources based on subject, difficulty progression, format preference, and tags.
- **Two Interfaces**:
  - **Web Interface**: A clean, user-friendly browser dashboard.
  - **Command-Line Interface (CLI)**: A simple text-based menu system.
- **User Profiles**: Track preferences, bookmarks, and learning history.
- **Easy Customization**: All resources and rules are stored in simple JSON files that anyone can edit.

## Project Structure

```
study_recommender/
├── README.md               # This documentation file
├── data/                   # Data files (Easy to modify!)
│   ├── resources.json      # The database of all study resources
│   ├── rules.json          # The weights and rules for the recommendation engine
│   └── profiles/           # User profiles and history (auto-generated)
├── src/                    # Source code
│   ├── recommender.py      # Core recommendation logic
│   ├── user_profile.py     # User tracking logic
│   ├── cli.py              # Command-line interface app
│   └── app.py              # Flask web server app
├── templates/              # Web interface HTML
│   └── index.html          # Main web page
└── static/                 # Web assets
    ├── css/style.css       # Stylesheet
    └── js/app.js           # Frontend logic
```

## Installation Guide

### Prerequisites
You need Python installed on your computer. You can download it from [python.org](https://www.python.org/).

### Step 1: Download the Project
Extract the provided ZIP file to a folder on your computer.

### Step 2: Install Required Packages
Open your terminal or command prompt, navigate to the project folder, and install Flask (needed for the web interface):

```bash
pip install flask
```
*(Note: If you only want to use the CLI version, no additional packages are required.)*

## How to Use the System

### Option 1: Web Interface (Recommended)
The web interface is the most user-friendly way to interact with the system.

1. Open your terminal or command prompt.
2. Navigate to the project folder.
3. Run the web server:
   ```bash
   python src/app.py
   ```
4. Open your web browser and go to: `http://localhost:5000`
5. Enter a username (e.g., "student1") to log in and start getting recommendations!

### Option 2: Command-Line Interface (CLI)
If you prefer a text-based experience:

1. Open your terminal or command prompt.
2. Navigate to the project folder.
3. Run the CLI app:
   ```bash
   python src/cli.py
   ```
4. Follow the on-screen menu instructions.

## How to Modify the System (For Students)

You don't need to be a programmer to customize this system! You can change how it works just by editing text files.

### 1. Adding New Resources
To add new books, videos, or courses, open `data/resources.json` in any text editor (like Notepad or VS Code) and add a new entry following this format:

```json
{
    "id": "res_009",
    "title": "My New Book",
    "type": "book",
    "subject": "science",
    "difficulty": "beginner",
    "format": "text",
    "duration_hours": 10,
    "url": "https://example.com",
    "tags": ["science", "basics"]
}
```
*Make sure every resource has a unique `id`!*

### 2. Changing Recommendation Rules
Want the system to care more about difficulty and less about the subject? Open `data/rules.json` and change the weights. 

```json
"weights": {
    "subject_match": 40,      // Change these numbers! (Should add up to 100)
    "difficulty_match": 30,
    "format_preference": 20,
    "tag_match": 10
}
```

You can also change the `minimum_score_threshold`. If you set it higher (e.g., 50), the system will only recommend items that are a very strong match.

### 3. Modifying Difficulty Progression
In `data/rules.json`, you can control what difficulty levels are recommended based on the user's current level:

```json
"difficulty_progression": {
    "beginner": ["beginner", "intermediate"],
    "intermediate": ["intermediate", "advanced"],
    "advanced": ["advanced"]
}
```
For example, if you change `"beginner": ["beginner"]`, beginners will *only* see beginner resources, never intermediate ones.

## Advanced Customization (For Coding Students)

If you want to modify the Python code, the core logic is in `src/recommender.py`. 
Look for the `_calculate_score` method to add entirely new rules to the recommendation algorithm!
