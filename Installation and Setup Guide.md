# Installation and Setup Guide

This guide will walk you through installing and running the Study Resource Recommender system on your computer.

## System Requirements

- **Python 3.7 or higher** (Download from [python.org](https://www.python.org/))
- **Windows, macOS, or Linux**
- **A web browser** (Chrome, Firefox, Safari, Edge, etc.)
- **A text editor** (Notepad, VS Code, Sublime Text, etc.)

## Step-by-Step Installation

### Step 1: Download and Extract the Project

1. Download the `study_recommender.zip` file
2. Extract it to a folder on your computer (e.g., `C:\Users\YourName\study_recommender` on Windows or `~/study_recommender` on Mac/Linux)

### Step 2: Open Terminal/Command Prompt

**On Windows:**
- Press `Win + R`, type `cmd`, and press Enter
- Navigate to your project folder: `cd C:\Users\YourName\study_recommender`

**On macOS/Linux:**
- Open Terminal (search for "Terminal" in Spotlight or Applications)
- Navigate to your project folder: `cd ~/study_recommender`

### Step 3: Install Python Dependencies

Run this command to install Flask (required for the web interface):

```bash
pip install -r requirements.txt
```

Or if the above doesn't work, try:

```bash
pip install flask
```

**Verify installation:**
```bash
python -c "import flask; print('Flask installed successfully!')"
```

## Running the Application

### Option 1: Web Interface (Recommended for Beginners)

The web interface is the easiest way to use the recommender system.

1. In your terminal, run:
   ```bash
   python src/app.py
   ```

2. You should see output like:
   ```
   * Running on http://127.0.0.1:5000
   ```

3. Open your web browser and go to: `http://localhost:5000`

4. You'll see the login page. Enter a username (e.g., "student1") and click "Login"

5. Start exploring recommendations!

**To stop the server:** Press `Ctrl + C` in your terminal

### Option 2: Command-Line Interface (CLI)

If you prefer a text-based menu system:

1. In your terminal, run:
   ```bash
   python src/cli.py
   ```

2. Follow the on-screen menu to navigate the system

3. To exit, select "Exit" from the menu

## Troubleshooting

### "Python is not recognized"
- **Windows:** Make sure Python is installed and added to your PATH. Reinstall Python and check "Add Python to PATH" during installation.
- **Mac/Linux:** Try `python3` instead of `python`

### "Flask is not installed"
Run this command:
```bash
pip install flask
```

If that doesn't work, try:
```bash
python -m pip install flask
```

### "Port 5000 is already in use"
If you get an error about port 5000 being in use:
1. Close any other instances of the app
2. Or modify `src/app.py` and change `port=5000` to `port=5001` (or another number)

### "Permission denied" error on Mac/Linux
Try running with `python3` instead of `python`:
```bash
python3 src/app.py
```

## First Time Setup Checklist

- [ ] Python installed and working
- [ ] Project extracted to a folder
- [ ] Opened terminal/command prompt
- [ ] Navigated to project folder
- [ ] Installed Flask with `pip install -r requirements.txt`
- [ ] Started the app with `python src/app.py` or `python src/cli.py`
- [ ] Successfully logged in with a username

## Next Steps

Once you have the system running, check out:
- **README.md** - Overview of features and project structure
- **CUSTOMIZATION_GUIDE.md** - How to modify resources and rules
- **API_DOCUMENTATION.md** - For advanced users who want to extend the system

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Make sure Python is properly installed
3. Verify you're in the correct project folder
4. Try closing and reopening your terminal
5. Restart your computer if all else fails

## Uninstalling

To remove the system:
1. Simply delete the project folder
2. Flask will remain installed, but it won't affect your system

To uninstall Flask:
```bash
pip uninstall flask
```
