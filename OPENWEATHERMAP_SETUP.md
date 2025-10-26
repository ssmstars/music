# 🌤️ OpenWeatherMap API Setup Guide (FREE)

## Why OpenWeatherMap?
- ✅ **100% FREE** for up to 1,000 API calls per day
- ✅ Already integrated in the project
- ✅ No credit card required
- ✅ Simple registration process

---

## 📝 Step-by-Step Setup (5 minutes)

### Step 1: Sign Up for Free Account

1. **Visit**: https://openweathermap.org/api
2. Click **"Sign Up"** or **"Get API Key"**
3. Fill in the registration form:
   - Email address
   - Username
   - Password
4. Click **"Create Account"**
5. **Verify your email** (check inbox/spam)

### Step 2: Get Your FREE API Key

1. After email verification, log in to: https://home.openweathermap.org/api_keys
2. You'll see your **default API key** already generated
3. **Copy the API key** (it looks like: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6`)

**Note**: It may take 10-15 minutes for the API key to activate. Be patient!

### Step 3: Add API Key to Your Project

**Option 1: Direct Edit (Quick)**

1. Open file: `weather_recommendation.py`
2. Find line 19:
   ```python
   self.api_key = api_key or "YOUR_OPENWEATHERMAP_API_KEY"
   ```
3. Replace with your actual key:
   ```python
   self.api_key = api_key or "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
   ```
4. Save the file

**Option 2: Environment Variable (Recommended)**

1. Open `app.py`
2. Add at the top after imports:
   ```python
   import os
   ```
3. When initializing WeatherMusicRecommender, pass the API key:
   ```python
   weather_recommender = WeatherMusicRecommender(df, api_key="YOUR_API_KEY_HERE")
   ```

### Step 4: Test Your API Key

1. **Restart the Flask application**:
   ```bash
   python app.py
   ```

2. **Open browser**: http://127.0.0.1:5000

3. **Test weather feature**:
   - Click "Discover Weather Music"
   - Allow location access
   - You should see **real weather data** for your location!

4. **Check terminal output**:
   - If API key is invalid, you'll see: `Weather API Error: 401`
   - If successful, you'll see weather data displayed

---

## 🎯 What You Get with FREE Plan

- **Calls per day**: 1,000 calls/day (more than enough!)
- **Current weather data**: ✅
- **Temperature**: ✅
- **Weather conditions**: ✅ (Clear, Rain, Clouds, etc.)
- **City name**: ✅
- **Country code**: ✅
- **Humidity**: ✅
- **No credit card required**: ✅

---

## 🔍 API Endpoint Being Used

```python
url = "https://api.openweathermap.org/data/2.5/weather"
params = {
    'lat': latitude,
    'lon': longitude,
    'appid': YOUR_API_KEY,
    'units': 'metric'
}
```

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Weather API Error: 401"
**Solution**: 
- API key not activated yet (wait 10-15 minutes)
- Wrong API key copied (check for spaces)

### Issue 2: "Demo City (API Key Required)" displayed
**Solution**: 
- API key not set correctly
- Check `weather_recommendation.py` line 19

### Issue 3: Location not detecting
**Solution**: 
- Enable location permissions in browser
- Try different browser (Chrome/Firefox/Edge)

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Get API key
Visit: https://openweathermap.org/api → Sign Up → Copy API Key

# 2. Add to project
Open: weather_recommendation.py
Edit line 19: self.api_key = api_key or "YOUR_KEY_HERE"

# 3. Restart app
python app.py

# 4. Test
Open browser → http://127.0.0.1:5000 → Click "Discover Weather Music"
```

---

## 📚 Additional Resources

- **OpenWeatherMap Documentation**: https://openweathermap.org/current
- **API Dashboard**: https://home.openweathermap.org/
- **FAQ**: https://openweathermap.org/faq

---

## 💡 Pro Tips

1. **Save your API key** in a safe place (text file, password manager)
2. **Don't share** your API key publicly
3. **Add to .gitignore** if using version control (already configured)
4. **Monitor usage** at: https://home.openweathermap.org/

---

## ✅ Verification Checklist

- [ ] Signed up at OpenWeatherMap
- [ ] Email verified
- [ ] API key copied
- [ ] Added to `weather_recommendation.py`
- [ ] Restarted application
- [ ] Tested weather feature
- [ ] Real city name displays (not "Demo City")

---

**Once set up, your weather-based music recommendations will use REAL-TIME weather data from your actual location!** 🌤️🎵

---

**Need Help?** 
- OpenWeatherMap Support: https://openweathermap.org/faq
- Check project README.md for more details
