# 🎵 Dynamic Tune - One Place for All

**Your Complete AI-Powered Music Platform**

An intelligent music ecosystem that combines machine learning recommendations, real-time weather analysis, AI song generation, and AI-powered lyrics creation - all in one beautiful, modern web application. Built as a 5th Semester AIML Mini Project.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![Machine Learning](https://img.shields.io/badge/ML-Scikit--learn-orange.svg)
![AI Powered](https://img.shields.io/badge/AI-Powered-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 What Makes This Special?

**Dynamic Tune** is not just another music recommendation system - it's a comprehensive platform that brings together:
- 🎯 **Smart Recommendations** powered by Machine Learning
- 🌤️ **Weather-Based Playlists** that match your environment
- 🎼 **AI Song Generation** via Suno AI integration
- ✍️ **AI Lyrics Creation** through Toolbaz integration
- 🎵 **Direct Music Playback** on Spotify and YouTube Music

**Truly ONE PLACE FOR ALL your music needs!**

## ✨ Complete Feature Set

### 🧠 AI-Powered Music Recommendations
- **Content-Based Filtering**: Advanced TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
- **Cosine Similarity Analysis**: Analyzes song features, lyrics, genres, and moods
- **Real-time Search**: Autocomplete search with instant suggestions
- **High Accuracy**: Personalized recommendations based on comprehensive song characteristics
- **Similarity Scoring**: Visual percentage match for each recommendation

### 🌤️ Weather-Based Music Discovery (Signature Feature)
- **Automatic Location Detection**: Browser-based GPS geolocation
- **Real-Time Weather Analysis**: Live integration with OpenWeatherMap API
- **Smart Mood Mapping**: Intelligently matches weather conditions to music moods
- **Dynamic Playlists**: Curated playlists that adapt to your current weather
- **Location Display**: Shows city name and country code
- **Weather Details**: Temperature, feels-like, humidity, and conditions

### 🎵 Music Platform Integration
- **Spotify Integration**: Direct "Play on Spotify" buttons for each song
- **YouTube Music Integration**: Instant "Play on YouTube Music" buttons
- **One-Click Playback**: Opens songs directly in your preferred music platform
- **Smart Search**: Automatically searches for song + artist combination
- **New Tab Opening**: Non-disruptive music streaming experience

### 🎼 AI Music Generation (Suno AI)
- **Create Original Songs**: Transform ideas into complete tracks
- **Text-to-Music**: Describe your vision and let AI compose
- **Professional Quality**: Studio-quality output with vocals and instruments
- **Multiple Genres**: Support for various music styles
- **Instant Creation**: Generate songs in minutes
- **Direct Integration**: Seamless redirect to Suno AI platform

### ✍️ AI Lyrics Generation (Toolbaz)
- **AI-Powered Writing**: Generate creative and meaningful lyrics
- **Genre-Specific**: Tailored lyrics for different music genres
- **Custom Themes**: Create lyrics based on your chosen theme
- **Rhyme & Structure**: Proper lyrical structure and rhyme schemes
- **Multiple Moods**: Adapt lyrics to different emotional tones
- **Easy Integration**: Direct access to Toolbaz lyric generator

### 🎨 Modern UI/UX Experience
- **Glassmorphism Design**: Beautiful frosted glass-effect cards
- **Gradient Animations**: Smooth color transitions and effects
- **Responsive Layout**: Perfect display on desktop, tablet, and mobile
- **Smooth Animations**: Engaging fade-in and hover effects
- **Dark Theme**: Eye-friendly dark mode interface
- **Intuitive Navigation**: Easy-to-use menu and section navigation
- **Loading States**: Professional loading indicators
- **Interactive Cards**: Hover effects and smooth transitions

### 🔄 Complete Creative Workflow
1. **Discover** → Find music through AI recommendations
2. **Generate** → Create original lyrics with AI
3. **Create** → Produce complete songs with Suno AI
4. **Play** → Listen on Spotify or YouTube Music

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Internet connection (for weather API and AI tools)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project.git
cd "AI-and-weather-Based-Music-Recommendation-System---Mini-Project"
```

2. **Install required packages**
```bash
pip install -r requirements.txt
```

3. **Configure OpenWeatherMap API** (For weather-based recommendations)
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key (Free tier: 1,000 calls/day)
   - Open `weather_recommendation.py`
   - Replace the API key on line 19:
   ```python
   self.api_key = "your_api_key_here"
   ```

4. **Run the application**
```bash
python app.py
```

5. **Access the platform**
   - Open your browser
   - Navigate to `http://127.0.0.1:5000`
   - Grant location permission for weather features
   - Explore all features!

### Available URLs
- Local: `http://127.0.0.1:5000`
- Network: `http://<your-ip>:5000` (accessible on local network)

## 📁 Project Structure

```
Mini Project 5th sem/
├── app.py                          # Flask application (main entry point)
├── recommendation.py               # Music recommendation engine (TF-IDF + Cosine Similarity)
├── weather_recommendation.py       # Weather-based recommendation system
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── data/
│   └── music_data.csv             # Music dataset (songs, artists, genres, moods, lyrics)
├── templates/
│   └── index.html                 # Main HTML template
└── static/
    ├── css/
    │   └── style.css              # Modern styling with animations
    └── js/
        └── script.js              # Frontend JavaScript logic
```

## 🔧 Technical Implementation

### Music Recommendation Algorithm

#### 1. Data Preprocessing
```python
# Combine all text features
combined_features = song + ' ' + artist + ' ' + genre + ' ' + mood + ' ' + lyrics

# Clean and normalize text
- Convert to lowercase
- Remove special characters
- Handle missing values
```

#### 2. TF-IDF Vectorization
```python
TfidfVectorizer(
    max_features=5000,      # Top 5000 features
    ngram_range=(1, 2),     # Unigrams and bigrams
    stop_words='english'    # Remove common words
)

# Creates 84 × 1517 feature matrix
```

#### 3. Similarity Computation
```python
# Cosine similarity between all songs
cosine_similarity(tfidf_matrix)

# Returns similarity scores (0-1)
# 1 = identical, 0 = completely different
```

#### 4. Recommendation Generation
```python
# Get top N similar songs
# Exclude the query song itself
# Sort by similarity score
# Return with metadata
```

### Weather Integration Flow

1. **Browser Geolocation** → User's GPS coordinates
2. **OpenWeatherMap API Call** → Current weather data
3. **Condition Analysis** → Weather → Mood mapping
4. **Playlist Filtering** → Filter by mood/genre
5. **Recommendation Display** → Curated playlist

### Weather-Mood Mapping
```python
{
    'Clear': ['happy', 'energetic'],
    'Clouds': ['calm', 'indie'],
    'Rain': ['melancholic', 'jazz', 'blues'],
    'Drizzle': ['calm', 'acoustic'],
    'Thunderstorm': ['energetic', 'rock'],
    'Snow': ['peaceful', 'classical'],
    'Mist/Fog': ['ambient', 'calm']
}
```

## 🎯 How to Use

### 1. Song-Based Recommendations 🎵
1. Navigate to "Song-Based Recommendations" section
2. Type a song name in the search box
3. Select from real-time autocomplete suggestions
4. Click **"Get Recommendations"**
5. Browse AI-curated recommendations with similarity scores
6. Click **Spotify** or **YouTube Music** buttons to play any song

### 2. Weather-Based Recommendations 🌤️
1. Scroll to "Weather-Based Recommendations"
2. Click **"Discover Weather Music"**
3. Allow location access when prompted
4. View your current weather, location, and mood
5. Explore weather-matched playlist
6. Play songs directly on Spotify or YouTube Music

### 3. AI Song Generation with Suno AI 🎼
1. Navigate to "AI Tools" section
2. Read about Suno AI's capabilities
3. Click **"Start Creating Music with Suno AI"**
4. You'll be redirected to Suno AI platform
5. Describe your song idea
6. Let AI compose, arrange, and produce your track
7. Download and share your creation!

### 4. AI Lyrics Generation with Toolbaz ✍️
1. Go to "AI Tools" section
2. Find the Toolbaz Lyrics Generator card
3. Click **"Generate Lyrics with AI"**
4. You'll be redirected to Toolbaz platform
5. Choose your genre and theme
6. Customize mood and style
7. Generate creative, rhyming lyrics instantly!

### Complete Creative Workflow 🔄
- **Step 1**: Discover songs that inspire you (Recommendations)
- **Step 2**: Generate original lyrics for your song (Toolbaz)
- **Step 3**: Create complete music with your lyrics (Suno AI)
- **Step 4**: Share your masterpiece with the world!

## 🛠️ Technologies Used

### Backend Technologies
- **Flask 3.0.0**: Modern Python web framework
- **Pandas 2.1.3**: Data manipulation and analysis
- **NumPy 1.26.2**: Numerical computing
- **Scikit-learn 1.3.2**: Machine learning algorithms
  - TF-IDF Vectorization (max_features=5000, ngram_range=(1,2))
  - Cosine Similarity for recommendation engine
- **Requests**: HTTP library for API calls

### Frontend Technologies
- **HTML5**: Semantic structure
- **CSS3**: Modern styling
  - Glassmorphism effects with backdrop-filter
  - CSS Grid and Flexbox layouts
  - CSS Custom Properties (Variables)
  - Keyframe animations
- **JavaScript ES6+**: Client-side functionality
  - Async/Await for API calls
  - Geolocation API
  - DOM manipulation
  - Event handling
- **Font Awesome 6.4.0**: Professional icon library

### External APIs & Services
- **OpenWeatherMap API**: Real-time weather data
  - Current weather conditions
  - Temperature and humidity
  - Location-based data
- **Suno AI**: AI music generation platform
  - Text-to-music conversion
  - Professional quality output
- **Toolbaz Lyric Generator**: AI-powered lyrics creation
  - Genre-specific lyrics
  - Rhyme and structure generation
- **Spotify Web**: Music streaming platform integration
- **YouTube Music**: Alternative streaming platform

### Development Tools
- **Git**: Version control
- **GitHub**: Repository hosting
- **VS Code**: Development environment
- **Python Virtual Environment**: Dependency isolation

## 📊 Dataset

The `music_data.csv` contains **84 curated songs** with comprehensive metadata:

### Dataset Structure
- **Song Name**: Title of the track
- **Artist**: Performer or band name
- **Genre**: Musical genre (Pop, Rock, Jazz, Hip-Hop, Classical, etc.)
- **Mood**: Emotional tone (Happy, Sad, Energetic, Calm, Romantic, etc.)
- **Lyrics**: Key lyrics, themes, and keywords for TF-IDF analysis

### Dataset Statistics
- **Total Songs**: 84
- **Feature Matrix Dimensions**: 84 × 1517
- **TF-IDF Features**: 5000 max features with bigrams
- **Genres Covered**: 10+ different genres
- **Mood Categories**: 8+ distinct moods

### Expanding the Dataset
You can easily add more songs by editing `data/music_data.csv`:
```csv
song,artist,genre,mood,lyrics
Your Song Title,Your Artist,pop,happy,"keywords themes emotions from the song"
```

**Note**: After adding songs, restart the application to rebuild the recommendation model.

## 🎨 Customization Guide

### Adding More Songs
1. Open `data/music_data.csv`
2. Add rows following this format:
```csv
song,artist,genre,mood,lyrics
Perfect,Ed Sheeran,pop,romantic,"love heart dance tonight sweet"
```
3. Save the file
4. Restart the application

### Modifying Weather-Mood Mappings
Edit `weather_recommendation.py`:
```python
self.weather_mood_map = {
    'Clear': ['your_mood_1', 'your_mood_2'],
    'Rain': ['your_custom_mood'],
    # Add more mappings
}
```

### Customizing UI Colors
Edit `static/css/style.css`:
```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    --accent-color: #your-color;
    /* Modify other CSS variables */
}
```

### Changing Port Number
Edit `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)  # Your port
```

### Adding More Weather Icons
Edit `static/js/script.js` in the `getWeatherIcon()` function:
```javascript
const icons = {
    'YourCondition': '<i class="fas fa-your-icon"></i>',
    // Add more conditions
};
```

## 🔐 API Keys & Configuration

### OpenWeatherMap API Setup

1. **Create Account**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Click "Sign Up" and create a free account
   - Verify your email address

2. **Get API Key**
   - Go to API Keys section in your account
   - Copy your default API key or create a new one
   - Free tier includes 1,000 API calls per day

3. **Configure Application**
   - Open `weather_recommendation.py`
   - Find line 19:
   ```python
   self.api_key = "782e98aa47114ab48de111603252110"  # Replace this
   ```
   - Replace with your API key:
   ```python
   self.api_key = "your_actual_api_key_here"
   ```
   - Save the file

4. **Test Weather Feature**
   - Restart the Flask application
   - Click "Discover Weather Music"
   - Check if weather data loads correctly

### API Rate Limits
- **OpenWeatherMap Free Tier**: 1,000 calls/day, 60 calls/minute
- **Suno AI**: Refer to Suno AI website for pricing
- **Toolbaz**: Check Toolbaz for current limits

### Security Best Practices
- Never commit API keys to public repositories
- Use environment variables for production:
```python
import os
self.api_key = os.getenv('OPENWEATHER_API_KEY', 'default_key')
```
- Rotate API keys periodically
- Monitor API usage in provider dashboard

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Dataset Not Found Error
```
Error: FileNotFoundError: music_data.csv not found
```
**Solution**: 
- Ensure `data/music_data.csv` exists in the project directory
- Check the file path in `app.py` (line ~15)
- Verify the data folder structure

#### Weather Feature Not Working
```
Error: Weather API Error 401 (Unauthorized)
```
**Solution**:
- Verify your OpenWeatherMap API key is correct
- Check that the API key is properly set in `weather_recommendation.py`
- Ensure your API key is activated (can take a few hours)
- Verify internet connection

#### Location Permission Denied
```
Error: Unable to access your location
```
**Solution**:
- Enable location services in your browser settings
- Grant permission when prompted
- Check browser privacy settings
- Try using HTTPS if available

#### Module Import Errors
```
Error: ModuleNotFoundError: No module named 'flask'
```
**Solution**:
```bash
pip install -r requirements.txt
```
Or install individually:
```bash
pip install flask pandas numpy scikit-learn requests
```

#### Port Already in Use
```
Error: Address already in use
```
**Solution**:
- Change port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```
- Or kill the process using port 5000:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

#### Spotify/YouTube Buttons Not Working
**Solution**:
- Ensure JavaScript is enabled in browser
- Check browser console for errors (F12)
- Verify Font Awesome icons are loading
- Clear browser cache and reload

#### Recommendations Not Displaying
**Solution**:
- Check browser console for JavaScript errors
- Verify the Flask server is running
- Ensure the dataset loaded successfully (check terminal output)
- Try with a different song name

## 📈 Future Enhancements

### Planned Features
- 🔐 **User Authentication**: Login system with personalized profiles
- 💾 **Playlist Management**: Save, edit, and organize favorite playlists
- 📊 **Listening Analytics**: Track listening history and generate insights
- 🎧 **Real Spotify Playback**: Embed Spotify player for in-app playback
- 🔄 **Collaborative Filtering**: User-based recommendations using listening history
- 🤖 **Deep Learning Models**: Neural networks for advanced recommendations
- 🌍 **Multi-language Support**: International language support
- 📱 **Mobile App**: Native iOS and Android applications
- 🎤 **Voice Control**: Voice commands for hands-free operation
- 📲 **Social Sharing**: Share playlists and recommendations with friends
- � **Theme Customization**: Multiple color themes and dark/light mode toggle
- 📡 **Offline Mode**: Cache recommendations for offline access
- 🎵 **Audio Preview**: 30-second song previews before streaming
- 📈 **Trending Charts**: Popular songs and rising recommendations
- 🔔 **Push Notifications**: New recommendation alerts

### Potential Integrations
- Apple Music API
- SoundCloud API
- Last.fm scrobbling
- Discord Rich Presence
- Twitter/X sharing
- Instagram Stories integration

### Technical Improvements
- Implement caching for faster recommendations
- Add database support (PostgreSQL/MongoDB)
- Implement RESTful API endpoints
- Add GraphQL support
- Docker containerization
- CI/CD pipeline setup
- Unit and integration testing
- Performance optimization
- CDN integration for static assets

## 🎓 Educational Value

### Learning Outcomes
This project demonstrates:
- **Machine Learning**: TF-IDF, Cosine Similarity, Content-based filtering
- **Web Development**: Full-stack development with Flask
- **API Integration**: Third-party API consumption and handling
- **Frontend Development**: Modern CSS, JavaScript, responsive design
- **Data Processing**: Pandas, NumPy for data manipulation
- **User Experience**: Intuitive UI/UX design principles
- **Version Control**: Git and GitHub workflow
- **Problem Solving**: Real-world application development

### Key Concepts Covered
1. **Natural Language Processing**: Text vectorization and analysis
2. **Recommendation Systems**: Content-based filtering algorithms
3. **RESTful APIs**: Building and consuming web APIs
4. **Asynchronous Programming**: JavaScript async/await patterns
5. **Responsive Design**: Mobile-first web design
6. **Data Visualization**: Presenting information effectively
7. **Software Architecture**: MVC-like pattern in Flask

### Academic Context
- **Course**: 5th Semester AIML (Artificial Intelligence & Machine Learning)
- **Project Type**: Mini Project
- **Duration**: One semester
- **Team Size**: Individual/Group project
- **Technologies**: Python, Flask, ML, Web Development

## 📸 Screenshots

### Home Page
Beautiful landing page with glassmorphism effects and smooth animations

### Song Recommendations
AI-powered recommendations with similarity scores and platform integration

### Weather-Based Playlists
Real-time weather detection with mood-matched music suggestions

### AI Tools Section
Integrated Suno AI and Toolbaz for complete creative workflow

### Music Platform Integration
Direct Spotify and YouTube Music playback buttons on every song

*Note: Add screenshots to enhance README visual appeal*

## 🏆 Project Highlights

### What Makes It Stand Out
✅ **Complete Ecosystem** - Not just recommendations, but a full music platform  
✅ **Real-World Integration** - Weather API, Spotify, YouTube, Suno AI, Toolbaz  
✅ **Modern Tech Stack** - Latest versions of Flask, Scikit-learn, and web technologies  
✅ **Professional UI** - Production-quality design with glassmorphism  
✅ **Practical ML** - Real application of machine learning algorithms  
✅ **User-Centric** - Intuitive interface with smooth user experience  
✅ **Scalable Architecture** - Well-structured code for future enhancements  
✅ **Comprehensive Documentation** - Detailed README and inline comments  

### Innovation Points
1. **Weather-Music Correlation**: Unique feature connecting environment to music taste
2. **Multi-Platform Integration**: Seamless connection to multiple music services
3. **AI Creative Tools**: Integration of cutting-edge AI generation platforms
4. **Complete Workflow**: End-to-end music discovery and creation pipeline
5. **One-Stop Solution**: "One Place for All" - truly comprehensive platform

## 🤝 Contributing

We welcome contributions to improve Dynamic Tune! This project is open for enhancements and bug fixes.

### How to Contribute

1. **Fork the Repository**
   ```bash
   # Click 'Fork' button on GitHub
   ```

2. **Clone Your Fork**
   ```bash
   git clone https://github.com/your-username/AI-and-weather-Based-Music-Recommendation-System---Mini-Project.git
   cd AI-and-weather-Based-Music-Recommendation-System---Mini-Project
   ```

3. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style
   - Test your changes thoroughly

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: Your descriptive commit message"
   ```

6. **Push to Your Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Describe your changes clearly
   - Wait for review

### Contribution Guidelines
- Follow PEP 8 style guide for Python code
- Write meaningful commit messages
- Add comments for complex logic
- Update documentation for new features
- Test before submitting pull requests
- Be respectful and constructive

### Areas for Contribution
- 🐛 Bug fixes and error handling
- ✨ New features and enhancements
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- ⚡ Performance optimizations
- 🌍 Internationalization
- 🧪 Unit tests and test coverage

## ⭐ Star History

If you find this project helpful, please consider giving it a star! ⭐

It helps others discover the project and motivates continued development.

## �📄 License

This project is created for educational purposes as part of a **5th Semester AIML Mini Project**.

### MIT License

Copyright (c) 2025 Dynamic Tune

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🙏 Acknowledgments

### Inspiration & Resources
- Original concept inspired by [harteij19/music-recommendation-app-python](https://github.com/harteij19/music-recommendation-app-python)
- **OpenWeatherMap** for comprehensive weather API
- **Scikit-learn** team for excellent ML algorithms and documentation
- **Flask** community for the lightweight web framework
- **Suno AI** for revolutionary AI music generation
- **Toolbaz** for AI-powered lyric generation tools
- **Spotify** and **YouTube Music** for music streaming platforms

### Special Thanks
- Faculty mentors for guidance and support
- AIML department for project opportunity
- Open-source community for tools and libraries
- Stack Overflow community for problem-solving help
- GitHub for hosting and collaboration tools

### Technologies Acknowledgment
We're grateful to the creators and maintainers of:
- Python Programming Language
- NumPy and Pandas libraries
- Font Awesome icon library
- Unsplash for high-quality images
- VS Code development environment

## 📧 Contact & Support

### Project Repository
🔗 [GitHub Repository](https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project)

### Get Help
- 🐛 **Report Bugs**: [Open an Issue](https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project/issues)
- 💡 **Feature Requests**: [Create a Feature Request](https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project/issues)
- 📖 **Documentation**: Check this README and inline code comments
- 💬 **Discussions**: Use GitHub Discussions for questions

### Developer
- **GitHub**: [@hvkr15](https://github.com/hvkr15)
- **Project**: 5th Semester AIML Mini Project
- **Year**: 2025

---

<div align="center">

### 🎵 **Dynamic Tune - One Place for All** 🎵

**Discover • Create • Generate • Play**

Built with ❤️ using AI, ML, and Modern Web Technologies

*Combining Machine Learning with Real-World Data for Intelligent Music Discovery and Creation*

**[⭐ Star this repository](https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project)** | **[🐛 Report Bug](https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project/issues)** | **[✨ Request Feature](https://github.com/hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project/issues)**

---

**Made with 💙 for 5th Semester AIML Mini Project 2025**

</div>
