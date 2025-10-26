# Quick Start Guide

## 🚀 Run the Application

### Option 1: Double-click start.bat
Simply double-click the `start.bat` file in Windows Explorer.

### Option 2: Using PowerShell/Command Prompt
```bash
python app.py
```

### Option 3: With detailed output
```bash
python -u app.py
```

## 📝 First Time Setup

1. **Install Dependencies** (if not already done)
   ```bash
   pip install -r requirements.txt
   ```

2. **Get Weather API Key** (Optional)
   - Visit https://openweathermap.org/api
   - Sign up for free account
   - Copy your API key
   - Open `weather_recommendation.py`
   - Replace `YOUR_OPENWEATHERMAP_API_KEY` with your actual key

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Open Browser**
   - Go to: http://127.0.0.1:5000
   - Enable location permissions for weather features

## 🎵 Using the System

### Song Recommendations
1. Type a song name in the search box
2. Select from autocomplete results
3. Click "Get Recommendations"

### Weather-Based Recommendations
1. Click "Discover Weather Music"
2. Allow location access
3. Get personalized weather-matched playlist

## 🔧 Troubleshooting

**Port already in use?**
Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Missing dependencies?**
```bash
pip install -r requirements.txt
```

**Dataset not found?**
Ensure `data/music_data.csv` exists

## 📚 Learn More

See README.md for full documentation.
