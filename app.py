from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import pandas as pd
import os
from recommendation import MusicRecommender
from spotify_recommender import SpotifyMusicRecommender
from weather_recommendation import WeatherMusicRecommender

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Demo user credentials (In production, use a database with hashed passwords)
DEMO_USERS = {
    'admin': 'admin123',
    'user': 'user123'
}

# Initialize recommenders
music_recommender = None
weather_recommender = None
use_spotify_dataset = False

def load_data():
    """Load music dataset and initialize recommenders"""
    global music_recommender, weather_recommender, use_spotify_dataset
    try:
        # Try to load Spotify Million Song Dataset first
        if os.path.exists('data/spotify_million_songs.csv'):
            print("📊 Loading Spotify Million Song Dataset...")
            df = pd.read_csv('data/spotify_million_songs.csv')
            
            # Use Spotify recommender for the large dataset
            music_recommender = SpotifyMusicRecommender(df)
            use_spotify_dataset = True
            print("✓ Spotify dataset loaded successfully!")
            
            # For weather recommendations, use original dataset if available
            # Otherwise, create a simple weather-based recommender with Spotify data
            if os.path.exists('data/music_data.csv'):
                print("📊 Loading original dataset for weather recommendations...")
                weather_df = pd.read_csv('data/music_data.csv')
                weather_recommender = WeatherMusicRecommender(weather_df)
                print("✓ Weather recommender initialized with original dataset!")
            else:
                print("ℹ️  Weather-based recommendations disabled (original dataset not found)")
                weather_recommender = None
            
            return True
            
        # Fallback to original dataset
        elif os.path.exists('data/music_data.csv'):
            print("📊 Loading original music dataset...")
            df = pd.read_csv('data/music_data.csv')
            music_recommender = MusicRecommender(df)
            weather_recommender = WeatherMusicRecommender(df)
            use_spotify_dataset = False
            print("✓ Original dataset loaded successfully!")
            return True
            
        else:
            print("⚠ Warning: No dataset found. Please add dataset.")
            return False
            
    except Exception as e:
        print(f"Error loading data: {e}")
        import traceback
        traceback.print_exc()
        return False

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page route"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate credentials
        if username in DEMO_USERS and DEMO_USERS[username] == password:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    # If already logged in, redirect to home
    if session.get('logged_in'):
        return redirect(url_for('home'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout route"""
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def home():
    """Home page route"""
    return render_template('index.html')

@app.route('/lyrics-generator')
def lyrics_generator():
    """Lyrics Generator page route"""
    return render_template('lyrics_generator.html')

@app.route('/song-creator')
def song_creator():
    """Song Creator page route"""
    return render_template('song_creator.html')

@app.route('/song-generator')
def song_generator():
    """Song Generator page route"""
    return render_template('song_generator.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    """Get music recommendations based on selected song"""
    try:
        data = request.get_json()
        song_name = data.get('song_name', '')
        languages = data.get('languages', ['all'])  # Get multiple languages from request
        
        if not music_recommender:
            return jsonify({'error': 'System not initialized. Please check dataset.'}), 500
        
        # Convert languages list to language filter
        language_filter = None
        if languages and 'all' not in languages:
            language_filter = languages
        
        # Pass language filter to recommendation function
        recommendations = music_recommender.get_recommendations(
            song_name, 
            n_recommendations=10,
            language_filter=language_filter
        )
        
        if recommendations is None or len(recommendations) == 0:
            return jsonify({'error': 'Song not found or no recommendations available'}), 404
        
        return jsonify({
            'success': True,
            'recommendations': recommendations.to_dict('records')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/weather-recommend', methods=['POST'])
def weather_recommend():
    """Get music recommendations based on current weather"""
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        languages = data.get('languages', ['all'])  # Get multiple languages from request
        
        if not weather_recommender:
            return jsonify({
                'success': False,
                'error': 'Weather-based recommendations are currently unavailable. Please ensure the original music dataset (music_data.csv) is present.'
            }), 503
        
        # Convert languages list to language filter
        language_filter = None
        if languages and 'all' not in languages:
            language_filter = languages
        
        result = weather_recommender.get_weather_based_recommendations(
            latitude, longitude, n_recommendations=15,
            language_filter=language_filter
        )
        
        if result is None:
            return jsonify({
                'success': False,
                'error': 'Unable to fetch weather data. Please check your internet connection or try again later.'
            }), 500
        
        return jsonify({
            'success': True,
            'weather': result['weather'],
            'mood': result['mood'],
            'recommendations': result['recommendations'].to_dict('records')
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'An error occurred: {str(e)}'
        }), 500

@app.route('/get-songs', methods=['GET'])
def get_songs():
    """Get list of all available songs"""
    try:
        if not music_recommender or music_recommender.df is None:
            return jsonify({'error': 'System not initialized'}), 500
        
        songs = music_recommender.df['song'].tolist()
        return jsonify({
            'success': True,
            'songs': songs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search-songs', methods=['GET'])
def search_songs():
    """Search songs by query"""
    try:
        query = request.args.get('q', '').lower()
        
        if not music_recommender or music_recommender.df is None:
            return jsonify({'error': 'System not initialized'}), 500
        
        if not query:
            songs = music_recommender.df['song'].head(50).tolist()
        else:
            songs = music_recommender.df[
                music_recommender.df['song'].str.lower().str.contains(query, na=False)
            ]['song'].head(50).tolist()
        
        return jsonify({
            'success': True,
            'songs': songs
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-languages', methods=['GET'])
def get_languages():
    """Get list of available languages in the dataset"""
    try:
        if not music_recommender or music_recommender.df is None:
            return jsonify({'error': 'System not initialized'}), 500
        
        # Get available languages
        if hasattr(music_recommender, 'get_available_languages'):
            languages = music_recommender.get_available_languages()
        elif 'language' in music_recommender.df.columns:
            languages = music_recommender.df['language'].dropna().unique().tolist()
            languages = sorted(languages)
        else:
            languages = []
        
        return jsonify({
            'success': True,
            'languages': languages
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-lyrics', methods=['POST'])
def generate_lyrics():
    """Generate AI lyrics based on user input"""
    try:
        data = request.get_json()
        theme = data.get('theme', '')
        language = data.get('language', 'english')
        genre = data.get('genre', 'pop')
        mood = data.get('mood', 'happy')
        verse_count = data.get('verseCount', 2)
        rhyme_scheme = data.get('rhymeScheme', 'AABB')
        song_length = data.get('songLength', 'medium')
        
        if not theme:
            return jsonify({'error': 'Theme is required'}), 400
        
        # Generate lyrics with enhanced parameters
        lyrics = generate_lyrics_template(theme, genre, mood, language, verse_count, rhyme_scheme, song_length)
        
        return jsonify({
            'success': True,
            'lyrics': lyrics,
            'theme': theme,
            'genre': genre,
            'mood': mood,
            'language': language,
            'verseCount': verse_count,
            'rhymeScheme': rhyme_scheme,
            'songLength': song_length
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-song', methods=['POST'])
def generate_song():
    """Generate AI song description based on user input"""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        duration = data.get('duration', 'medium')
        tempo = data.get('tempo', 'medium')
        vocals = data.get('vocals', 'mixed')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Generate song description
        song_description = generate_song_description(prompt, duration, tempo, vocals)
        
        return jsonify({
            'success': True,
            'song_description': song_description,
            'prompt': prompt
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_song_description(prompt, duration, tempo, vocals):
    """Generate detailed song description for AI music platforms"""
    
    # Map tempo to BPM range
    tempo_map = {
        'slow': '60-80 BPM',
        'medium': '90-120 BPM',
        'fast': '130-160 BPM'
    }
    
    # Map duration to structure
    duration_map = {
        'short': 'Intro → Verse → Chorus → Verse → Chorus → Outro',
        'medium': 'Intro → Verse 1 → Chorus → Verse 2 → Chorus → Bridge → Final Chorus → Outro',
        'long': 'Intro → Verse 1 → Pre-Chorus → Chorus → Verse 2 → Pre-Chorus → Chorus → Bridge → Instrumental Break → Final Chorus → Extended Outro'
    }
    
    # Analyze the prompt to extract key elements
    prompt_lower = prompt.lower()
    
    # Detect genre hints
    genre_hints = []
    if any(word in prompt_lower for word in ['rock', 'guitar', 'drums', 'electric']):
        genre_hints.append('Rock')
    if any(word in prompt_lower for word in ['pop', 'catchy', 'upbeat', 'radio']):
        genre_hints.append('Pop')
    if any(word in prompt_lower for word in ['electronic', 'edm', 'synth', 'beat']):
        genre_hints.append('Electronic')
    if any(word in prompt_lower for word in ['jazz', 'saxophone', 'swing']):
        genre_hints.append('Jazz')
    if any(word in prompt_lower for word in ['classical', 'orchestra', 'piano']):
        genre_hints.append('Classical')
    if any(word in prompt_lower for word in ['hip-hop', 'rap', 'trap', 'beats']):
        genre_hints.append('Hip-Hop')
    
    genre_text = ', '.join(genre_hints) if genre_hints else 'Contemporary'
    
    # Detect mood/emotion
    mood_hints = []
    if any(word in prompt_lower for word in ['happy', 'upbeat', 'cheerful', 'joyful', 'fun']):
        mood_hints.append('uplifting and energetic')
    if any(word in prompt_lower for word in ['sad', 'melancholic', 'emotional', 'heartbreak']):
        mood_hints.append('emotional and introspective')
    if any(word in prompt_lower for word in ['romantic', 'love', 'passion']):
        mood_hints.append('romantic and tender')
    if any(word in prompt_lower for word in ['aggressive', 'intense', 'powerful']):
        mood_hints.append('intense and powerful')
    if any(word in prompt_lower for word in ['calm', 'peaceful', 'relaxing', 'chill']):
        mood_hints.append('calm and soothing')
    
    mood_text = ', '.join(mood_hints) if mood_hints else 'balanced and expressive'
    
    # Detect instruments
    instruments = []
    if 'guitar' in prompt_lower:
        instruments.append('electric guitar' if 'electric' in prompt_lower else 'acoustic guitar')
    if any(word in prompt_lower for word in ['piano', 'keys', 'keyboard']):
        instruments.append('piano')
    if 'drums' in prompt_lower or 'percussion' in prompt_lower:
        instruments.append('dynamic drums and percussion')
    if any(word in prompt_lower for word in ['synth', 'electronic']):
        instruments.append('synthesizers')
    if 'bass' in prompt_lower:
        instruments.append('bass guitar')
    if 'strings' in prompt_lower or 'violin' in prompt_lower:
        instruments.append('string section')
    
    instruments_text = ', '.join(instruments) if instruments else 'varied instrumentation'
    
    # Build the description
    description = f"""🎵 AI SONG DESCRIPTION
{'=' * 60}

📋 ORIGINAL PROMPT:
{prompt}

{'=' * 60}

🎼 SONG SPECIFICATIONS:

Genre: {genre_text}
Mood/Emotion: {mood_text}
Tempo: {tempo.capitalize()} ({tempo_map[tempo]})
Duration: {duration.capitalize()}
Vocals: {vocals.capitalize()}

{'=' * 60}

🎹 MUSICAL ELEMENTS:

Main Instruments: {instruments_text}
Production Style: Modern, polished production with clear mix
Vocal Style: {'Professional studio vocals with emotion and clarity' if vocals != 'instrumental' else 'No vocals - purely instrumental'}

{'=' * 60}

🎭 SONG STRUCTURE:
{duration_map[duration]}

{'=' * 60}

✨ DETAILED DESCRIPTION FOR AI:

Create a {tempo.lower()}-tempo {genre_text.lower()} song with a {mood_text} vibe. 
The song should feature {instruments_text.lower()} as the primary sonic elements. 

{prompt}

The production should be modern and radio-ready, with a focus on:
- Clear and balanced mix
- Dynamic arrangement that builds throughout the song
- Professional mastering quality
- Attention to emotional delivery and atmosphere

{f"Vocal performance should be {vocals} with professional technique, clear articulation, and emotional depth appropriate to the song's theme." if vocals != 'instrumental' else "As an instrumental track, focus on melodic development and instrumental expression to convey emotion."}

Target a {duration.lower()} format suitable for streaming platforms, 
maintaining listener engagement throughout with varied sections and dynamic changes.

{'=' * 60}

💡 USE THIS DESCRIPTION:
Copy the detailed description above and paste it into AI music generation 
platforms like Suno AI, Udio, or MusicLM for best results!
"""
    
    return description

def generate_multilingual_lyrics(theme, genre, mood, language):
    """Generate lyrics in different Indian languages with multiple variations"""
    
    import random
    
    # Language-specific templates with multiple variations
    lyrics_templates = {
        'hindi': {
            'verses': [
                [
                    f"दिल में है {theme} की आग",
                    f"जो जलती है हर एक राग",
                    f"{theme} के साथ है ये सफर",
                    f"हर पल में मिले नया असर"
                ],
                [
                    f"{theme} की खुशबू हवा में",
                    f"बहती है रूह की दुआ में",
                    f"जिंदगी मिली है नई",
                    f"{theme} से हर खुशी पाई"
                ],
                [
                    f"चाँद सितारों से कहूँ",
                    f"{theme} की कहानी सुनाऊँ",
                    f"ये जो एहसास है मेरा",
                    f"{theme} तू ही है सवेरा"
                ],
                [
                    f"रंगों में {theme} बसा है",
                    f"हर खुशी में तू दिखा है",
                    f"सपनों का राजा बन गया",
                    f"{theme} से जीवन सजा है"
                ],
                [
                    f"धड़कनों में {theme} बसे",
                    f"हर सांस में तू रहे",
                    f"दिल की गहराइयों में",
                    f"{theme} तेरी परछाइयों में"
                ]
            ],
            'choruses': [
                [
                    f"ओ {theme}, तू ही है मेरी जान",
                    f"तेरे बिना अधूरी ये कहानी",
                    f"{theme} से है ये प्यार",
                    f"दिल की धड़कन, जीवन का आधार"
                ],
                [
                    f"{theme}, {theme}, दिल में बसे",
                    f"हर ख्वाब में तू ही नजर आए",
                    f"जीने की वजह तू ही है",
                    f"{theme} मेरा हर सुबह शाम"
                ],
                [
                    f"आजा {theme}, महफ़िल सजा दें",
                    f"मिल के हम ख़ुशी मना लें",
                    f"तेरे संग जीना है मुझे",
                    f"{theme}, तुझे पाना है मुझे"
                ]
            ],
            'bridges': [
                f"जब भी लगे अंधेरा\n{theme} बने सहारा मेरा",
                f"मंजिल भी तू, रास्ता भी तू\n{theme} मेरी हर दुआ में",
                f"आसमान को छू लें हम\n{theme} के साथ उड़ें बदलों में",
                f"तूफ़ान आए या हो बरसात\n{theme} संग है मेरी हर बात"
            ],
            'outros': [
                f"{theme}... {theme}...\nसदा रहे दिल में बसा",
                f"{theme} सदा के लिए\nमेरे साथ रहना",
                f"{theme}, हमेशा-हमेशा\nतू मेरा, मैं तेरा"
            ]
        },
        'kannada': {
            'verses': [
                [
                    f"{theme} ನನ್ನ ಹೃದಯದಲ್ಲಿ",
                    f"ಸದಾ ನಿನ್ನ ನೆನಪಿನಲ್ಲಿ",
                    f"{theme} ನೀನು ನನ್ನ ಜೀವನ",
                    f"ಪ್ರತಿ ಕ್ಷಣ ಹೊಸ ಸಂತೋಷ"
                ],
                [
                    f"ಆಕಾಶದ ನಕ್ಷತ್ರಗಳಲ್ಲಿ",
                    f"{theme} ನಿನ್ನ ಬೆಳಕು ಕಾಣುತ್ತೆ",
                    f"ಪ್ರತಿ ಹೊತ್ತು ಹೊಸ ಕನಸು",
                    f"{theme} ನೀನೇ ನನ್ನ ವಿಶ್ವಾಸ"
                ],
                [
                    f"ಗಾಳಿಯಲ್ಲಿ {theme} ವಾಸನೆ",
                    f"ಮಳೆಯಲ್ಲಿ ನಿನ್ನ ಸ್ಪರ್ಶ",
                    f"ಪ್ರಕೃತಿಯೂ ಹಾಡುತ್ತಿದೆ",
                    f"{theme} ನಮ್ಮ ಪ್ರೀತಿಯ ಗೀತೆ"
                ],
                [
                    f"ಬೆಳಗಿನ ಬೆಳಕಿನಲ್ಲಿ",
                    f"{theme} ನಿನ್ನ ಮುಗುಳ್ನಗೆ",
                    f"ಹೂವುಗಳು ಅರಳುತ್ತವೆ",
                    f"{theme} ನಮ್ಮ ಪ್ರೇಮದಿಂದ"
                ],
                [
                    f"ಕನಸಿನ ಲೋಕದಲ್ಲಿ",
                    f"{theme} ನೀನು ನನ್ನ ರಾಣಿ",
                    f"ಎಲ್ಲಾ ದುಃಖಗಳು ಮರೆತು",
                    f"{theme} ನೀನು ಮಾತ್ರ ನನ್ನದು"
                ]
            ],
            'choruses': [
                [
                    f"ಓ {theme}, ನೀನೇ ನನ್ನ ಪ್ರಾಣ",
                    f"ನಿನ್ನ ಬಿಟ್ಟು ಇಲ್ಲ ನನಗೆ ಸ್ಥಾನ",
                    f"{theme} ಯೊಂದಿಗೆ ಪ್ರೀತಿ",
                    f"ಹೃದಯದ ಗೀತೆ, ಜೀವನದ ರೀತಿ"
                ],
                [
                    f"{theme}, {theme}, ನನ್ನ ಎಲ್ಲವೂ",
                    f"ನಿನ್ನ ನಗುವೇ ನನ್ನ ಬೆಳಕು",
                    f"ಜೀವನವೇ ಸುಂದರ ಆಯಿತು",
                    f"{theme} ನೀನು ಬಂದ ಮೇಲೆ"
                ],
                [
                    f"ಬಾ {theme}, ನಮ್ಮ ಲೋಕ ಸೃಷ್ಟಿಸೋಣ",
                    f"ಒಟ್ಟಿಗೆ ನಾವು ಕನಸು ಕಾಣೋಣ",
                    f"ನಿನ್ನ ಜೊತೆ ಬದುಕಬೇಕು",
                    f"{theme}, ನಿನ್ನನ್ನೇ ಪಡೆಯಬೇಕು"
                ]
            ],
            'bridges': [
                f"ಕತ್ತಲು ಆವರಿಸಿದಾಗ\n{theme} ನೀನೇ ನನ್ನ ಬೆಳಕು",
                f"ದಾರಿಯೂ ನೀನೇ, ಗುರಿಯೂ ನೀನೇ\n{theme} ನನ್ನ ಎಲ್ಲಾ ಪ್ರಾರ್ಥನೆಯಲ್ಲಿ",
                f"ಚಂಡಮಾರುತ ಬಂದರೂ\n{theme} ನೀನು ನನ್ನ ಆಶ್ರಯ"
            ],
            'outros': [
                f"{theme}... {theme}...\nಎಂದೆಂದಿಗೂ ನನ್ನೊಂದಿಗೆ",
                f"{theme} ಸದಾಕಾಲ\nನನ್ನ ಜೊತೆಗಿರು",
                f"{theme}, ಎಂದೆಂದಿಗೂ\nನೀನು ನನ್ನದು, ನಾನು ನಿನ್ನದು"
            ]
        },
        'tamil': {
            'verses': [
                [
                    f"{theme} என் மனதில்",
                    f"நீ எப்போதும் நினைவில்",
                    f"{theme} நீயே என் வாழ்க்கை",
                    f"ஒவ்வொரு நொடியும் புதிய மகிழ்ச்சி"
                ],
                [
                    f"வானத்தில் நட்சத்திரங்கள்",
                    f"{theme} உன் ஒளி காண்கிறேன்",
                    f"ஒவ்வொரு கனவிலும்",
                    f"{theme} நீதான் என் நம்பிக்கை"
                ],
                [
                    f"காற்றில் {theme} வாசனை",
                    f"மழையில் உன் தொடுதல்",
                    f"இயற்கையும் பாடுகிறது",
                    f"{theme} நம் காதல் பாடலை"
                ]
            ],
            'choruses': [
                [
                    f"ஓ {theme}, நீதான் என் உயிர்",
                    f"உன்னை விட்டால் எனக்கு இடமில்லை",
                    f"{theme} உடன் காதல்",
                    f"இதயத்தின் பாட்டு, வாழ்க்கையின் வழி"
                ],
                [
                    f"{theme}, {theme}, என் அனைத்தும்",
                    f"உன் புன்னகையே என் ஒளி",
                    f"வாழ்க்கை அழகாக ஆனது",
                    f"{theme} நீ வந்த பிறகு"
                ]
            ],
            'bridges': [
                f"இருள் சூழும் போது\n{theme} நீயே என் ஒளி",
                f"பாதையும் நீதான், இலக்கும் நீதான்\n{theme} என் எல்லா பிரார்த்தனையிலும்"
            ],
            'outros': [
                f"{theme}... {theme}...\nஎன்றென்றும் என்னுடன்",
                f"{theme} எப்போதும்\nஎன்னோடு இரு"
            ]
        },
        'telugu': {
            'verses': [
                [
                    f"{theme} నా హృదయంలో",
                    f"నీవు ఎప్పుడూ జ్ఞాపకంలో",
                    f"{theme} నువ్వే నా జీవితం",
                    f"ప్రతి క్షణం కొత్త ఆనందం"
                ],
                [
                    f"ఆకాశంలో నక్షత్రాలలో",
                    f"{theme} నీ వెలుగు చూస్తున్నాను",
                    f"ప్రతి కలలో",
                    f"{theme} నువ్వే నా నమ్మకం"
                ],
                [
                    f"గాలిలో {theme} వాసన",
                    f"వానలో నీ స్పర్శ",
                    f"ప్రకృతి కూడా పాడుతోంది",
                    f"{theme} మన ప్రేమ గీతం"
                ]
            ],
            'choruses': [
                [
                    f"ఓ {theme}, నువ్వే నా ప్రాణం",
                    f"నిన్ను లేకుండా నాకు స్థానం లేదు",
                    f"{theme} తో ప్రేమ",
                    f"హృదయపు పాట, జీవిత మార్గం"
                ],
                [
                    f"{theme}, {theme}, నా అన్నీ",
                    f"నీ చిరునవ్వే నా వెలుగు",
                    f"జీవితం అందంగా అయింది",
                    f"{theme} నువ్వు వచ్చిన తర్వాత"
                ]
            ],
            'bridges': [
                f"చీకటి ఆవరించినప్పుడు\n{theme} నువ్వే నా వెలుగు",
                f"దారి కూడా నువ్వే, లక్ష్యం కూడా నువ్వే\n{theme} నా ప్రార్థనల్లో"
            ],
            'outros': [
                f"{theme}... {theme}...\nఎప్పటికీ నాతో",
                f"{theme} ఎల్లప్పుడూ\nనాతో ఉండు"
            ]
        },
        'malayalam': {
            'verses': [
                [
                    f"{theme} എന്റെ ഹൃദയത്തിൽ",
                    f"നീ എപ്പോഴും ഓർമ്മയിൽ",
                    f"{theme} നീയാണ് എന്റെ ജീവിതം",
                    f"ഓരോ നിമിഷവും പുതിയ സന്തോഷം"
                ],
                [
                    f"ആകാശത്തിലെ നക്ഷത്രങ്ങളിൽ",
                    f"{theme} നിന്റെ വെളിച്ചം കാണുന്നു",
                    f"ഓരോ സ്വപ്നത്തിലും",
                    f"{theme} നീയാണ് എന്റെ വിശ്വാസം"
                ],
                [
                    f"കാറ്റിൽ {theme} സുഗന്ധം",
                    f"മഴയിൽ നിന്റെ സ്പർശം",
                    f"പ്രകൃതിയും പാടുന്നു",
                    f"{theme} നമ്മുടെ പ്രണയഗാനം"
                ]
            ],
            'choruses': [
                [
                    f"ഓ {theme}, നീയാണ് എന്റെ പ്രാണൻ",
                    f"നിന്നെ കൂടാതെ എനിക്ക് സ്ഥലമില്ല",
                    f"{theme} യോടൊപ്പം സ്നേഹം",
                    f"ഹൃദയത്തിന്റെ പാട്ട്, ജീവിതത്തിന്റെ വഴി"
                ],
                [
                    f"{theme}, {theme}, എന്റെ എല്ലാം",
                    f"നിന്റെ പുഞ്ചിരിയാണ് എന്റെ വെളിച്ചം",
                    f"ജീവിതം മനോഹരമായി",
                    f"{theme} നീ വന്നതിനുശേഷം"
                ]
            ],
            'bridges': [
                f"ഇരുട്ട് വരുമ്പോൾ\n{theme} നീയാണ് എന്റെ വെളിച്ചം",
                f"വഴിയും നീയാണ്, ലക്ഷ്യവും നീയാണ്\n{theme} എന്റെ പ്രാർത്ഥനകളിൽ"
            ],
            'outros': [
                f"{theme}... {theme}...\nഎന്നെന്നേക്കും എന്നോടൊപ്പം",
                f"{theme} എപ്പോഴും\nഎന്നോടൊപ്പം ഉണ്ടായിരിക്കൂ"
            ]
        },
        'marathi': {
            'verses': [
                [
                    f"{theme} माझ्या हृदयात",
                    f"तू नेहमी आठवणीत",
                    f"{theme} तूच माझे जीवन",
                    f"प्रत्येक क्षण नवा आनंद"
                ],
                [
                    f"आकाशातल्या ताऱ्यांमध्ये",
                    f"{theme} तुझा प्रकाश दिसतो",
                    f"प्रत्येक स्वप्नात",
                    f"{theme} तूच माझा विश्वास"
                ],
                [
                    f"वाऱ्यात {theme} सुगंध",
                    f"पावसात तुझा स्पर्श",
                    f"निसर्गही गात आहे",
                    f"{theme} आपल्या प्रेमाचे गीत"
                ]
            ],
            'choruses': [
                [
                    f"ओ {theme}, तूच माझा प्राण",
                    f"तुझ्याशिवाय मला स्थान नाही",
                    f"{theme} सोबत प्रेम",
                    f"हृदयाचे गीत, जीवनाचा मार्ग"
                ],
                [
                    f"{theme}, {theme}, माझे सर्वस्व",
                    f"तुझे हास्य माझा प्रकाश",
                    f"जीवन सुंदर झाले",
                    f"{theme} तू आल्यानंतर"
                ]
            ],
            'bridges': [
                f"जेव्हा अंधार येतो\n{theme} तूच माझा प्रकाश",
                f"मार्गही तूच, ध्येयही तूच\n{theme} माझ्या प्रार्थनांमध्ये"
            ],
            'outros': [
                f"{theme}... {theme}...\nसदैव माझ्यासोबत",
                f"{theme} नेहमी\nमाझ्यासोबत रहा"
            ]
        },
        'bengali': {
            'verses': [
                [
                    f"{theme} আমার হৃদয়ে",
                    f"তুমি সর্বদা স্মৃতিতে",
                    f"{theme} তুমিই আমার জীবন",
                    f"প্রতি মুহূর্তে নতুন আনন্দ"
                ],
                [
                    f"আকাশের তারাদের মধ্যে",
                    f"{theme} তোমার আলো দেখি",
                    f"প্রতিটি স্বপ্নে",
                    f"{theme} তুমিই আমার বিশ্বাস"
                ],
                [
                    f"বাতাসে {theme} সুগন্ধ",
                    f"বৃষ্টিতে তোমার স্পর্শ",
                    f"প্রকৃতিও গাইছে",
                    f"{theme} আমাদের প্রেমের গান"
                ]
            ],
            'choruses': [
                [
                    f"ও {theme}, তুমিই আমার প্রাণ",
                    f"তোমাকে ছাড়া আমার কোনো স্থান নেই",
                    f"{theme} এর সাথে ভালোবাসা",
                    f"হৃদয়ের গান, জীবনের পথ"
                ],
                [
                    f"{theme}, {theme}, আমার সবকিছু",
                    f"তোমার হাসি আমার আলো",
                    f"জীবন সুন্দর হয়ে উঠেছে",
                    f"{theme} তুমি আসার পর"
                ]
            ],
            'bridges': [
                f"যখন অন্ধকার আসে\n{theme} তুমিই আমার আলো",
                f"পথও তুমি, লক্ষ্যও তুমি\n{theme} আমার প্রার্থনায়"
            ],
            'outros': [
                f"{theme}... {theme}...\nচিরকাল আমার সাথে",
                f"{theme} সবসময়\nআমার সাথে থাকো"
            ]
        },
        'punjabi': {
            'verses': [
                [
                    f"{theme} ਮੇਰੇ ਦਿਲ ਵਿੱਚ",
                    f"ਤੂੰ ਹਮੇਸ਼ਾ ਯਾਦਾਂ ਵਿੱਚ",
                    f"{theme} ਤੂੰ ਹੀ ਮੇਰੀ ਜ਼ਿੰਦਗੀ",
                    f"ਹਰ ਪਲ ਨਵੀਂ ਖੁਸ਼ੀ"
                ],
                [
                    f"ਅਸਮਾਨ ਦੇ ਤਾਰਿਆਂ ਵਿੱਚ",
                    f"{theme} ਤੇਰੀ ਰੌਸ਼ਨੀ ਦਿਖਦੀ",
                    f"ਹਰ ਸੁਪਨੇ ਵਿੱਚ",
                    f"{theme} ਤੂੰ ਹੀ ਮੇਰਾ ਵਿਸ਼ਵਾਸ"
                ],
                [
                    f"ਹਵਾ ਵਿੱਚ {theme} ਖੁਸ਼ਬੂ",
                    f"ਮੀਂਹ ਵਿੱਚ ਤੇਰਾ ਸਪਰਸ਼",
                    f"ਕੁਦਰਤ ਵੀ ਗਾ ਰਹੀ",
                    f"{theme} ਸਾਡੇ ਪਿਆਰ ਦਾ ਗੀਤ"
                ]
            ],
            'choruses': [
                [
                    f"ਓ {theme}, ਤੂੰ ਹੀ ਮੇਰੀ ਜਾਨ",
                    f"ਤੇਰੇ ਬਿਨਾ ਨਹੀਂ ਕੋਈ ਥਾਂ",
                    f"{theme} ਨਾਲ ਪਿਆਰ",
                    f"ਦਿਲ ਦਾ ਗੀਤ, ਜੀਵਨ ਦਾ ਰਾਹ"
                ],
                [
                    f"{theme}, {theme}, ਮੇਰਾ ਸਭ ਕੁਝ",
                    f"ਤੇਰੀ ਮੁਸਕਾਨ ਮੇਰੀ ਰੋਸ਼ਨੀ",
                    f"ਜ਼ਿੰਦਗੀ ਖੂਬਸੂਰਤ ਹੋ ਗਈ",
                    f"{theme} ਤੇਰੇ ਆਉਣ ਤੋਂ ਬਾਅਦ"
                ]
            ],
            'bridges': [
                f"ਜਦੋਂ ਹਨੇਰਾ ਆਵੇ\n{theme} ਤੂੰ ਹੀ ਮੇਰੀ ਰੋਸ਼ਨੀ",
                f"ਰਾਹ ਵੀ ਤੂੰ, ਮੰਜ਼ਿਲ ਵੀ ਤੂੰ\n{theme} ਮੇਰੀਆਂ ਪ੍ਰਾਰਥਨਾਵਾਂ ਵਿੱਚ"
            ],
            'outros': [
                f"{theme}... {theme}...\nਹਮੇਸ਼ਾ ਮੇਰੇ ਨਾਲ",
                f"{theme} ਸਦਾ\nਮੇਰੇ ਨਾਲ ਰਹਿ"
            ]
        },
        'gujarati': {
            'verses': [
                [
                    f"{theme} મારા હૃદયમાં",
                    f"તું હંમેશા યાદમાં",
                    f"{theme} તું જ મારું જીવન",
                    f"દરેક ક્ષણે નવો આનંદ"
                ],
                [
                    f"આકાશના તારાઓમાં",
                    f"{theme} તારો પ્રકાશ દેખાય",
                    f"દરેક સપનામાં",
                    f"{theme} તું જ મારો વિશ્વાસ"
                ],
                [
                    f"હવામાં {theme} સુગંધ",
                    f"વરસાદમાં તારો સ્પર્શ",
                    f"પ્રકૃતિ પણ ગાય છે",
                    f"{theme} આપણા પ્રેમનું ગીત"
                ]
            ],
            'choruses': [
                [
                    f"ઓ {theme}, તું જ મારો પ્રાણ",
                    f"તારા વિના મને સ્થાન નથી",
                    f"{theme} સાથે પ્રેમ",
                    f"હૃદયનું ગીત, જીવનનો માર્ગ"
                ],
                [
                    f"{theme}, {theme}, મારું બધું",
                    f"તારું સ્મિત મારો પ્રકાશ",
                    f"જીવન સુંદર બન્યું",
                    f"{theme} તું આવ્યા પછી"
                ]
            ],
            'bridges': [
                f"જ્યારે અંધકાર આવે\n{theme} તું જ મારો પ્રકાશ",
                f"માર્ગ પણ તું, લક્ષ્ય પણ તું\n{theme} મારી પ્રાર્થનાઓમાં"
            ],
            'outros': [
                f"{theme}... {theme}...\nસદા મારી સાથે",
                f"{theme} હંમેશા\nમારી સાથે રહે"
            ]
        }
    }
    
    template = lyrics_templates.get(language, lyrics_templates['hindi'])
    
    # Randomize selections for variety
    selected_verse1 = random.choice(template['verses'])
    selected_verse2 = random.choice([v for v in template['verses'] if v != selected_verse1])
    selected_verse3 = random.choice(template['verses'])
    
    selected_chorus = random.choice(template['choruses'])
    selected_bridge = random.choice(template['bridges'])
    selected_outro = random.choice(template['outros'])
    
    # Build lyrics structure
    lyrics = f"""[Verse 1]
{selected_verse1[0]}
{selected_verse1[1]}
{selected_verse1[2]}
{selected_verse1[3]}

[Chorus]
{selected_chorus[0]}
{selected_chorus[1]}
{selected_chorus[2]}
{selected_chorus[3]}

[Verse 2]
{selected_verse2[0]}
{selected_verse2[1]}
{selected_verse2[2]}
{selected_verse2[3]}

[Chorus]
{selected_chorus[0]}
{selected_chorus[1]}
{selected_chorus[2]}
{selected_chorus[3]}

[Verse 3]
{selected_verse3[0]}
{selected_verse3[1]}
{selected_verse3[2]}
{selected_verse3[3]}

[Chorus]
{selected_chorus[0]}
{selected_chorus[1]}
{selected_chorus[2]}
{selected_chorus[3]}

[Bridge]
{selected_bridge}

[Final Chorus]
{selected_chorus[0]}
{selected_chorus[1]}
{selected_chorus[2]}
{selected_chorus[3]}

[Outro]
{selected_outro}
"""
    
    return lyrics

def generate_lyrics_template(theme, genre, mood, language='english', verse_count=2, rhyme_scheme='AABB', song_length='medium'):
    """Generate lyrics using templates based on genre, mood, and language with enhanced variety"""
    
    # If language is not English, generate transliterated/regional lyrics
    if language != 'english':
        return generate_multilingual_lyrics(theme, genre, mood, language)
    
    import random
    
    # Expanded mood-based verse templates with more variety
    verse_templates = {
        'happy': [
            [
                f"When I think about {theme}, my heart starts to glow",
                f"Every moment with {theme}, letting feelings flow",
                f"Dancing through the day, {theme} lights my way",
                f"Nothing can compare to this joy I display"
            ],
            [
                f"Sunshine and {theme}, that's all I need",
                f"With {theme} in my life, I'm finally freed",
                f"Smiling all day long, everything feels right",
                f"{theme} makes my world so bright"
            ],
            [
                f"Can't stop the feeling when {theme} comes around",
                f"My feet lift off, barely touching the ground",
                f"Pure happiness flows, like a river so wide",
                f"With {theme} here, I've got nothing to hide"
            ],
            [
                f"Wake up every morning with {theme} on my mind",
                f"Leaving all my worries and troubles behind",
                f"Life's a celebration when {theme}'s by my side",
                f"Riding on this joyful, colorful tide"
            ],
            [
                f"Laughter echoes when {theme} fills the air",
                f"Magic moments happening everywhere",
                f"Jumping, spinning, feeling so alive",
                f"With {theme}, I truly thrive"
            ]
        ],
        'sad': [
            [
                f"Memories of {theme} fade like morning dew",
                f"Lost in thoughts of {theme}, feeling so blue",
                f"Searching for the light, through the darkest night",
                f"Hoping {theme} will make things right"
            ],
            [
                f"Empty spaces where {theme} used to be",
                f"Tears fall down like rain, I can barely see",
                f"The silence screams so loud, in this lonely room",
                f"Without {theme}, I'm consumed by gloom"
            ],
            [
                f"I reach for {theme}, but you're not there",
                f"The weight of loss is more than I can bear",
                f"Each day gets harder, the pain won't fade",
                f"In the shadow of {theme}, memories cascade"
            ],
            [
                f"Walking alone, thinking of {theme}",
                f"Nothing's quite as perfect as it used to seem",
                f"The photographs remind me of what we had",
                f"Now {theme}'s a ghost, making me sad"
            ],
            [
                f"Cold winds blow where {theme} once was warm",
                f"I'm caught up in this emotional storm",
                f"Broken pieces scattered on the floor",
                f"{theme}'s not here, not anymore"
            ]
        ],
        'energetic': [
            [
                f"Let's go, {theme} is calling out my name",
                f"Feel the beat, {theme} sets my soul aflame",
                f"No stopping now, we're breaking all the chains",
                f"Living for {theme}, running through the veins"
            ],
            [
                f"Jump up high, {theme} gives me wings to fly",
                f"Electric energy, reaching for the sky",
                f"Can't slow down now, we're on a roll",
                f"{theme}'s got control of my heart and soul"
            ],
            [
                f"Adrenaline rush when {theme} comes alive",
                f"Feel the power surge, ready to dive",
                f"No limits here, we're breaking through the wall",
                f"With {theme} beside me, I'll never fall"
            ],
            [
                f"Pulse is racing, {theme} in my blood",
                f"Can't contain this unstoppable flood",
                f"We're charging forward, no looking back",
                f"{theme} keeps me on the attack"
            ],
            [
                f"Lightning strikes when {theme} takes the stage",
                f"Unleashing power, breaking out the cage",
                f"Faster, stronger, we're reaching new heights",
                f"{theme} ignites these endless nights"
            ]
        ],
        'calm': [
            [
                f"Peaceful moments with {theme} by my side",
                f"Gentle whispers where {theme} resides",
                f"In the stillness, {theme} helps me find",
                f"A quiet place within my mind"
            ],
            [
                f"Soft as a breeze, {theme} flows through me",
                f"In this tranquil space, I'm finally free",
                f"No rush, no noise, just pure serenity",
                f"{theme} brings me to infinity"
            ],
            [
                f"Like water flowing over smooth stones",
                f"{theme} calms my restless bones",
                f"In meditation, I find my way",
                f"With {theme}, I'll be okay"
            ],
            [
                f"Silence speaks when {theme} is near",
                f"All my anxious thoughts disappear",
                f"Breathing slowly, peace within",
                f"{theme} lets the healing begin"
            ],
            [
                f"Moonlight dances with {theme} tonight",
                f"Everything feels perfectly right",
                f"Floating gently on this peaceful stream",
                f"{theme} fulfills my every dream"
            ]
        ],
        'romantic': [
            [
                f"Your {theme} touches me like poetry in motion",
                f"Drowning in waves of sweet emotion",
                f"Every heartbeat whispers your name",
                f"With {theme}, I'll never be the same"
            ],
            [
                f"Candlelight and {theme}, dancing close tonight",
                f"Lost in your eyes, everything feels right",
                f"This love we share, so pure and true",
                f"My {theme}, it's only you"
            ],
            [
                f"When you bring {theme} into my life",
                f"All the struggles, all the strife",
                f"They fade away like stars at dawn",
                f"With your {theme}, I carry on"
            ],
            [
                f"Roses bloom when {theme} calls my name",
                f"Setting my entire world aflame",
                f"In your arms is where I belong",
                f"{theme} makes my heart so strong"
            ],
            [
                f"Forever starts with {theme} and you",
                f"A love so deep, a bond so true",
                f"Hand in hand through thick and thin",
                f"{theme} is where we begin"
            ]
        ],
        'melancholic': [
            [
                f"Gray skies mirror how I feel about {theme}",
                f"Nothing's quite as perfect as it seems",
                f"Bittersweet memories linger in my mind",
                f"{theme}'s a treasure I can't find"
            ],
            [
                f"Autumn leaves and {theme}, both slip away",
                f"I'm holding on to yesterday",
                f"The sweetness tinged with sorrow and regret",
                f"{theme}'s something I can't forget"
            ],
            [
                f"Walking through the rain, thinking of {theme}",
                f"Life's not always what it seems",
                f"Beautiful and broken, that's how I feel",
                f"This {theme} is bittersweet but real"
            ],
            [
                f"Fading photographs of {theme} and I",
                f"Time moves on, but memories won't die",
                f"Caught between the laughter and the tears",
                f"{theme} haunts me through the years"
            ],
            [
                f"Twilight falls on {theme} once more",
                f"Longing for what came before",
                f"Sweet sadness fills my weary soul",
                f"{theme} takes its gentle toll"
            ]
        ],
        'angry': [
            [
                f"Fire and fury when {theme} comes to mind",
                f"I won't back down, won't be confined",
                f"Breaking through the walls they built around",
                f"With {theme}, I stand my ground"
            ],
            [
                f"Had enough of lies about {theme}",
                f"Time to scream, time to make a scene",
                f"This rage inside won't be contained",
                f"By {theme}, I won't be chained"
            ],
            [
                f"Burning bridges, {theme} lights the flame",
                f"I'm done playing this twisted game",
                f"No more holding back what I feel",
                f"{theme} makes this anger real"
            ],
            [
                f"Storm is coming, {theme} in my veins",
                f"Shattering these heavy chains",
                f"Thunder roars as I break free",
                f"{theme} unleashed the beast in me"
            ]
        ],
        'nostalgic': [
            [
                f"Remember when {theme} was all we knew",
                f"Those golden days when life was new",
                f"Time moves on, but memories stay",
                f"{theme} won't fade away"
            ],
            [
                f"Old photographs of {theme} in my hand",
                f"Takes me back to that distant land",
                f"If I could turn back time, I would",
                f"Relive {theme} if I could"
            ],
            [
                f"Dust-covered albums tell the tale",
                f"Of {theme} beyond the veil",
                f"Sepia-toned dreams of long ago",
                f"{theme} in that nostalgic glow"
            ],
            [
                f"Echoes of {theme} from years gone by",
                f"Make me laugh and make me cry",
                f"Wishing I could go back there",
                f"To {theme} beyond compare"
            ]
        ],
        'hopeful': [
            [
                f"Tomorrow brings {theme} shining bright",
                f"Even through the darkest night",
                f"I believe in better days ahead",
                f"By {theme}, I'll be led"
            ],
            [
                f"Seeds of {theme} we plant today",
                f"Will bloom and grow along the way",
                f"Keep the faith, don't let it go",
                f"{theme} will help us grow"
            ],
            [
                f"Dawn is breaking, {theme} appears",
                f"Washing away all my fears",
                f"A brand new chapter starts today",
                f"{theme} lights the way"
            ],
            [
                f"Rising from the ashes with {theme}",
                f"Building castles from broken dreams",
                f"Every setback makes me stronger still",
                f"{theme} bends but never breaks my will"
            ]
        ],
        'mysterious': [
            [
                f"Shadows dance around {theme} tonight",
                f"Secrets hidden just out of sight",
                f"In the darkness, whispers call",
                f"{theme} enchants us all"
            ],
            [
                f"Like a riddle wrapped in {theme}",
                f"Nothing's ever as it seems",
                f"Cryptic messages in the air",
                f"{theme}'s mystery everywhere"
            ],
            [
                f"Moonlight reveals what {theme} conceals",
                f"Ancient secrets it reveals",
                f"In the mist, I hear your name",
                f"{theme} plays a mystic game"
            ],
            [
                f"Veiled in wonder, {theme} appears",
                f"Speaking truths that no one hears",
                f"Enigmatic, undefined",
                f"{theme} puzzles every mind"
            ]
        ],
        'empowering': [
            [
                f"Stand up tall, {theme} makes me strong",
                f"I've had the power all along",
                f"No one can hold me down no more",
                f"With {theme}, watch me soar"
            ],
            [
                f"I am the storm, I am {theme}",
                f"Stronger than I've ever been",
                f"Unbreakable, I rise again",
                f"{theme} flows through my veins"
            ],
            [
                f"Warrior spirit, {theme} is my shield",
                f"On this battlefield, I'll never yield",
                f"Crown upon my head, I reign",
                f"{theme} is my domain"
            ],
            [
                f"Mountains bow before my {theme}",
                f"I'm the master of my dream",
                f"Fearless, bold, I claim my throne",
                f"With {theme}, I stand alone"
            ],
            [
                f"Phoenix rising with {theme} inside",
                f"No more running, no more hide",
                f"I am power, I am might",
                f"{theme} is my birthright"
            ]
        ]
    }
    
    # Expanded genre-based chorus templates
    chorus_templates = {
        'pop': [
            [
                f"Oh {theme}, you're everything I need",
                f"{theme}, you're the one who sets me free",
                f"Together we can fly so high",
                f"With {theme}, reaching for the sky"
            ],
            [
                f"{theme}, {theme}, can't get you off my mind",
                f"You're one of a kind, so hard to find",
                f"Baby, you're my perfect melody",
                f"{theme}'s all I need to be"
            ],
            [
                f"Ooh-ooh, {theme} lights up my world",
                f"Like a precious pearl unfurled",
                f"Dancing to the rhythm of our hearts",
                f"{theme}, you're where my story starts"
            ]
        ],
        'rock': [
            [
                f"{theme}! Breaking through the night!",
                f"{theme}! We're ready for the fight!",
                f"Nothing's gonna hold us back!",
                f"With {theme}, we're on the attack!"
            ],
            [
                f"We're loud and proud with {theme}",
                f"Living like we're in a dream",
                f"Turn it up, break the sound",
                f"{theme}'s the best we've found!"
            ],
            [
                f"Screaming out for {theme} tonight",
                f"We're gonna make this moment right",
                f"Guitars blazing, drums so loud",
                f"{theme} makes us proud!"
            ]
        ],
        'jazz': [
            [
                f"{theme} in the moonlight, soft and slow",
                f"Swaying to the rhythm, letting feelings show",
                f"In this jazzy paradise we've found",
                f"With {theme}, love knows no bound"
            ]
        ],
        'hip-hop': [
            [
                f"Yeah, {theme} on my mind all day",
                f"Living life my own unique way",
                f"{theme} got me feeling so fly",
                f"Reaching for the stars up in the sky"
            ],
            [
                f"Check it, {theme} running through my head",
                f"Moving forward, never looking back instead",
                f"Got that flow, got that vibe so clean",
                f"{theme}'s the best you've ever seen"
            ]
        ],
        'rap': [
            [
                f"Yo, {theme} in my DNA, can't deny",
                f"Spitting bars so high, watching haters cry",
                f"I'm the realest in the game, that's a fact",
                f"{theme}'s my weapon in this rap attack"
            ]
        ],
        'trap': [
            [
                f"{theme} got me flexing, yeah (flexing, yeah)",
                f"Bass so heavy, feel it in your chest-ing, yeah",
                f"We don't stop, keep it going all night",
                f"{theme} shining bright, we ignite"
            ]
        ],
        'r&b': [
            [
                f"Oh baby, {theme}'s what I'm craving tonight",
                f"Your love feels so right, holding me tight",
                f"Smooth like silk, sweet like wine",
                f"{theme}, you're forever mine"
            ]
        ],
        'country': [
            [
                f"Down that dusty road with {theme} in my heart",
                f"Been together from the very start",
                f"Through the fields and the summer rain",
                f"{theme} eases all my pain"
            ]
        ],
        'folk': [
            [
                f"Gather 'round and hear the tale of {theme}",
                f"Passed down through time like a precious dream",
                f"Simple truths in every word we sing",
                f"{theme}'s the wisdom that we bring"
            ]
        ],
        'indie': [
            [
                f"In my own little world with {theme}",
                f"Nothing's quite as perfect as it seems",
                f"But I don't care what they all say",
                f"{theme} guides me my own way"
            ]
        ],
        'alternative': [
            [
                f"Strange and beautiful, that's {theme} to me",
                f"Different from what others see",
                f"I walk a path that's all my own",
                f"With {theme}, I've grown"
            ]
        ],
        'edm': [
            [
                f"Feel the drop when {theme} hits the floor",
                f"Hands up high, we're craving more",
                f"Electric hearts beating as one",
                f"With {theme}, we've just begun"
            ]
        ],
        'house': [
            [
                f"Four on the floor with {theme} in the air",
                f"Dancing without a single care",
                f"The groove goes on throughout the night",
                f"{theme} feels so right"
            ]
        ],
        'techno': [
            [
                f"Synthetic dreams of {theme} tonight",
                f"Pulsing beats and laser light",
                f"Lost in the machine's embrace",
                f"{theme} takes me to another place"
            ]
        ],
        'classical': [
            [
                f"Like a symphony, {theme} plays divine",
                f"Each note perfect, each phrase refined",
                f"Timeless beauty in every sound",
                f"In {theme}, peace is found"
            ]
        ],
        'blues': [
            [
                f"Got those {theme} blues deep in my soul",
                f"This feeling's got complete control",
                f"Twelve bars of truth, can't hide the pain",
                f"{theme}'s running through my veins like rain"
            ]
        ],
        'reggae': [
            [
                f"One love, one {theme}, feel the beat",
                f"Moving to the rhythm, can't stay in my seat",
                f"Positive vibrations all around",
                f"With {theme}, peace is found"
            ]
        ],
        'metal': [
            [
                f"Crushing riffs and {theme} in the pit!",
                f"We're never gonna quit, this is it!",
                f"Headbanging fury, raw and real!",
                f"{theme}'s made of steel!"
            ]
        ],
        'punk': [
            [
                f"Three chords and {theme}, that's all we need",
                f"Fighting the system, we won't concede",
                f"Raw and loud, we stand our ground",
                f"With {theme}, freedom's found!"
            ]
        ],
        'gospel': [
            [
                f"Hallelujah! {theme} sets me free",
                f"Grace and glory for all to see",
                f"Lift your voices, sing and praise",
                f"{theme} brightens all my days"
            ]
        ],
        'bollywood': [
            [
                f"Dil mein hai {theme}, oh my love",
                f"Sent from the heavens above",
                f"Dance and celebrate all night long",
                f"{theme}'s our Bollywood song"
            ]
        ],
        'k-pop': [
            [
                f"{theme}, {theme}, you make my heart go boom",
                f"Light up every single room",
                f"So kawaii, can't resist",
                f"{theme}, you top my list"
            ]
        ]
    }
    
    # Bridge templates
    bridge_templates = [
        f"When the world feels cold and gray\n{theme} shows me the way\nThrough the highs and through the lows\n{theme}'s the melody that flows",
        f"Close your eyes and feel it now\n{theme} will show you how\nTo break free from all your chains\n{theme} runs through your veins",
        f"In this moment, here and now\n{theme} teaches me somehow\nThat the journey's worth the fight\nWith {theme}, we'll be alright",
        f"Time stands still when {theme}'s around\nLost and found in every sound\nThis is where I'm meant to be\n{theme} has set me free",
        f"Everything changes with {theme}\nNothing stays the same it seems\nEvolution of the heart\n{theme} gave me a brand new start",
        f"Can you hear the call of {theme}\nEchoing through everything\nPast and future intertwine\n{theme} makes this moment mine",
        f"Rising up with {theme} inside\nNo more reasons left to hide\nAuthentic, raw, and true\n{theme} brought me back to you",
        f"In the silence, {theme} speaks loud\nStanding tall above the crowd\nThis connection can't be denied\n{theme}'s my eternal guide"
    ]
    
    # Select templates based on mood and genre (with randomization for variety)
    verses_list = verse_templates.get(mood, verse_templates['happy'])
    chorus_list = chorus_templates.get(genre, chorus_templates['pop'])
    
    # Randomize selection for variety
    selected_verses = random.choice(verses_list)
    selected_chorus = random.choice(chorus_list)
    selected_bridge = random.choice(bridge_templates)
    
    # Build the complete lyrics based on verse count and song length
    lyrics_parts = ["[Verse 1]"]
    lyrics_parts.append('\n'.join(selected_verses))
    lyrics_parts.append("\n\n[Chorus]")
    lyrics_parts.append('\n'.join(selected_chorus))
    
    # Add additional verses based on verse_count
    for i in range(2, min(verse_count + 1, 5)):  # Max 4 verses
        lyrics_parts.append(f"\n\n[Verse {i}]")
        # Create variation for additional verses
        if len(verses_list) > 1:
            alt_verses = random.choice([v for v in verses_list if v != selected_verses])
            lyrics_parts.append('\n'.join(alt_verses))
        else:
            # Use thematic variation
            lyrics_parts.append(f"The rhythm of {theme} pulses through my soul\nWith every beat, {theme} makes me whole\nCan you feel the magic in the air?\n{theme}'s presence everywhere")
        
        lyrics_parts.append("\n\n[Chorus]")
        lyrics_parts.append('\n'.join(selected_chorus))
    
    # Add bridge for medium/long songs
    if song_length in ['medium', 'long']:
        lyrics_parts.append("\n\n[Bridge]")
        lyrics_parts.append(selected_bridge)
        
        lyrics_parts.append("\n\n[Final Chorus]")
        lyrics_parts.append('\n'.join(selected_chorus))
    
    # Add outro for long songs
    if song_length == 'long':
        lyrics_parts.append(f"\n\n[Outro]")
        lyrics_parts.append(f"{theme}... {theme}...\nForever in my heart, {theme}\nThis is just the start, {theme}")
    else:
        lyrics_parts.append(f"\n\n[Outro]")
        lyrics_parts.append(f"{theme}... {theme}...\nForever in my heart, {theme}")
    
    return '\n'.join(lyrics_parts)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# Add lazy loading for first request (Vercel compatible)
_data_loaded = False

@app.before_request
def ensure_data_loaded():
    """Ensure data is loaded before handling any request"""
    global music_recommender, _data_loaded
    if not _data_loaded:
        try:
            load_data()
            _data_loaded = True
        except Exception as e:
            print(f"Error loading data: {e}")
            _data_loaded = False

if __name__ == '__main__':
    print("=" * 60)
    print("🎵 DYNAMIC TUNE - Music Recommendation System")
    print("=" * 60)
    
    # Load data
    if load_data():
        print("\n🚀 Starting server...")
        print("📍 Open http://127.0.0.1:5001 in your browser")
        print("=" * 60)
        # Disable debug mode for production use with large dataset
        # Debug mode causes double loading of dataset
        app.run(debug=False, host='0.0.0.0', port=5001)  # Changed port to 5001
    else:
        print("\n❌ Failed to start: Dataset not found")
        print("Please add 'data/music_data.csv' and restart")
        print("=" * 60)
