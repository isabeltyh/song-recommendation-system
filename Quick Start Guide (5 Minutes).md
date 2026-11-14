# Quick Start Guide (5 Minutes)

Get the Study Resource Recommender running in just 5 minutes!

## Prerequisites
- Python installed on your computer
- A web browser

## Step 1: Download and Extract (1 minute)
1. Download the `study_recommender.zip` file
2. Extract it to a folder on your computer

## Step 2: Install (1 minute)
Open terminal/command prompt and navigate to the folder:

```bash
cd path/to/study_recommender
pip install -r requirements.txt
```

## Step 3: Run (1 minute)
Choose one:

**Option A: Web Interface (Recommended)**
```bash
python src/app.py
```
Then open: `http://localhost:5000`

**Option B: Command-Line**
```bash
python src/cli.py
```

## Step 4: Use (2 minutes)
1. Enter a username (e.g., "student1")
2. Click "Get Recommendations"
3. See personalized study resources!

## What You Can Do

### In the Web Interface
- **Recommendations Tab** - Get personalized suggestions
- **Preferences Tab** - Change your learning preferences
- **Bookmarks Tab** - Save resources for later
- **History Tab** - See what you've viewed
- **All Resources Tab** - Browse everything

### In the CLI
- Navigate menus to explore resources
- Update preferences
- View recommendations
- Track bookmarks

## Customize (No Coding!)

### Add a Resource
1. Open `data/resources.json` in a text editor
2. Add a new entry following the format
3. Refresh your browser or restart the app

### Change Recommendation Rules
1. Open `data/rules.json`
2. Adjust the weights (numbers should add to 100)
3. Refresh your browser or restart the app

See `CUSTOMIZATION_GUIDE.md` for details.

## Troubleshooting

**"Port 5000 is already in use"**
- Edit `src/app.py` and change `port=5000` to `port=5001`

**"Flask not installed"**
- Run: `pip install flask`

**"Python not found"**
- Make sure Python is installed
- Try `python3` instead of `python`

## Next Steps

1. Read `README.md` for feature overview
2. Check `CUSTOMIZATION_GUIDE.md` to modify resources
3. Explore `API_DOCUMENTATION.md` for advanced usage

## Need Help?

- **Installation issues?** → See `INSTALLATION_GUIDE.md`
- **Want to customize?** → See `CUSTOMIZATION_GUIDE.md`
- **Building something custom?** → See `API_DOCUMENTATION.md`
- **General questions?** → See `README.md`

---

**Enjoy exploring study resources!** 📚
