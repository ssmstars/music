import requests
import pandas as pd
from datetime import datetime
from recommendation import MusicRecommender

class WeatherMusicRecommender:
    """
    Weather-based music recommendation system that suggests music based on current weather conditions
    """
    
    def __init__(self, df, api_key=None):
        """
        Initialize weather-based recommender
        
        Args:
            df: Pandas DataFrame containing music data
            api_key: OpenWeatherMap API key (optional, will use demo mode if not provided)
        """
        self.df = df
        self.api_key = api_key or "34dc98c68f184a59a5a5e93a2487fe58"  # OpenWeatherMap API key
        self.music_recommender = MusicRecommender(df)
        
        # Define weather to mood mappings
        self.weather_mood_map = {
            'Clear': 'happy',
            'Clouds': 'calm',
            'Rain': 'melancholic',
            'Drizzle': 'relaxed',
            'Thunderstorm': 'energetic',
            'Snow': 'peaceful',
            'Mist': 'calm',
            'Fog': 'calm',
            'Haze': 'relaxed',
            'Dust': 'neutral',
            'Sand': 'neutral',
            'Smoke': 'calm'
        }
        
        # Define temperature-based mood adjustments
        self.temp_mood_map = {
            'very_cold': 'cozy',      # < 0°C
            'cold': 'calm',            # 0-15°C
            'mild': 'relaxed',         # 15-25°C
            'warm': 'happy',           # 25-35°C
            'hot': 'energetic'         # > 35°C
        }
        
        # Genre suggestions based on weather
        self.weather_genre_map = {
            'Clear': ['pop', 'dance', 'electronic', 'reggae'],
            'Clouds': ['indie', 'folk', 'acoustic', 'ambient'],
            'Rain': ['jazz', 'blues', 'r&b', 'soul'],
            'Drizzle': ['indie', 'folk', 'acoustic', 'lo-fi'],
            'Thunderstorm': ['rock', 'metal', 'electronic', 'hip-hop'],
            'Snow': ['classical', 'ambient', 'indie', 'folk'],
            'Mist': ['ambient', 'electronic', 'chill', 'lo-fi'],
            'Fog': ['ambient', 'electronic', 'chill', 'lo-fi']
        }
    
    def get_weather_data(self, latitude, longitude):
        """
        Fetch current weather data from OpenWeatherMap API
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            
        Returns:
            Dictionary with weather information
        """
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Get city and country information
                city_name = data.get('name', 'Unknown Location')
                country_code = data.get('sys', {}).get('country', '')
                
                # Create full location name
                if country_code:
                    full_location = f"{city_name}, {country_code}"
                else:
                    full_location = city_name
                
                weather_info = {
                    'condition': data['weather'][0]['main'],
                    'description': data['weather'][0]['description'],
                    'temperature': data['main']['temp'],
                    'feels_like': data['main']['feels_like'],
                    'humidity': data['main']['humidity'],
                    'city': full_location,
                    'icon': data['weather'][0]['icon']
                }
                
                return weather_info
            else:
                print(f"Weather API Error: {response.status_code}")
                return self._get_demo_weather()
                
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return self._get_demo_weather()
    
    def _get_demo_weather(self):
        """Return demo weather data for testing"""
        return {
            'condition': 'Clear',
            'description': 'clear sky',
            'temperature': 25,
            'feels_like': 24,
            'humidity': 60,
            'city': 'Demo City (API Key Required)',
            'icon': '01d'
        }
    
    def _determine_mood_from_weather(self, weather_info):
        """
        Determine mood based on weather conditions
        
        Args:
            weather_info: Dictionary with weather data
            
        Returns:
            String representing the mood
        """
        # Get base mood from weather condition
        condition = weather_info['condition']
        base_mood = self.weather_mood_map.get(condition, 'neutral')
        
        # Adjust based on temperature
        temp = weather_info['temperature']
        if temp < 0:
            temp_mood = 'cozy'
        elif temp < 15:
            temp_mood = 'calm'
        elif temp < 25:
            temp_mood = 'relaxed'
        elif temp < 35:
            temp_mood = 'happy'
        else:
            temp_mood = 'energetic'
        
        # Combine moods (you can make this more sophisticated)
        return f"{base_mood} {temp_mood}"
    
    def get_weather_based_recommendations(self, latitude, longitude, n_recommendations=15, language_filter=None):
        """
        Get music recommendations based on current weather
        
        Args:
            latitude: Location latitude
            longitude: Location longitude
            n_recommendations: Number of songs to recommend
            language_filter: Optional language to filter recommendations (e.g., 'hindi', 'english', 'all')
            
        Returns:
            Dictionary with weather info and recommended songs
        """
        try:
            # Get weather data
            weather_info = self.get_weather_data(latitude, longitude)
            
            # Determine mood from weather
            mood = self._determine_mood_from_weather(weather_info)
            
            # Get recommended genres for this weather
            condition = weather_info['condition']
            preferred_genres = self.weather_genre_map.get(condition, ['pop', 'indie'])
            
            # Filter songs by mood and genre (with optional language filter)
            recommendations = self._filter_songs_by_weather(mood, preferred_genres, n_recommendations, language_filter)
            
            result = {
                'weather': weather_info,
                'mood': mood,
                'preferred_genres': preferred_genres,
                'recommendations': recommendations
            }
            
            return result
            
        except Exception as e:
            print(f"Error getting weather-based recommendations: {e}")
            return None
    
    def _filter_songs_by_weather(self, mood, preferred_genres, n_songs=15, language_filter=None):
        """
        Filter songs based on mood and preferred genres
        
        Args:
            mood: The determined mood
            preferred_genres: List of preferred genres
            n_songs: Number of songs to return
            language_filter: Optional language(s) to filter by - can be string or list
            
        Returns:
            DataFrame with recommended songs
        """
        filtered_songs = self.df.copy()
        
        # Filter by language first if specified
        if language_filter and 'language' in filtered_songs.columns:
            # Convert single language to list for uniform handling
            if isinstance(language_filter, str):
                languages = [language_filter]
            else:
                languages = language_filter
            
            # Filter out 'all' if present
            languages = [lang.lower() for lang in languages if lang.lower() != 'all']
            
            if languages:
                language_mask = filtered_songs['language'].str.lower().isin(languages)
                language_songs = filtered_songs[language_mask]
                
                if len(language_songs) > 0:
                    filtered_songs = language_songs
        
        # Filter by mood if mood column exists
        if 'mood' in filtered_songs.columns:
            mood_keywords = mood.lower().split()
            mood_mask = filtered_songs['mood'].str.lower().apply(
                lambda x: any(keyword in str(x).lower() for keyword in mood_keywords) if pd.notna(x) else False
            )
            mood_songs = filtered_songs[mood_mask]
            
            if len(mood_songs) > 0:
                filtered_songs = mood_songs
        
        # Filter by genre if genre column exists
        if 'genre' in filtered_songs.columns and len(preferred_genres) > 0:
            genre_mask = filtered_songs['genre'].str.lower().apply(
                lambda x: any(genre in str(x).lower() for genre in preferred_genres) if pd.notna(x) else False
            )
            genre_songs = filtered_songs[genre_mask]
            
            if len(genre_songs) > 0:
                filtered_songs = genre_songs
        
        # If we have enough songs, return them
        if len(filtered_songs) >= n_songs:
            return filtered_songs.sample(n=min(n_songs, len(filtered_songs)))
        else:
            # If not enough, add random songs to reach n_songs (respecting language filter if set)
            remaining = n_songs - len(filtered_songs)
            
            if language_filter and 'language' in self.df.columns:
                # Convert single language to list for uniform handling
                if isinstance(language_filter, str):
                    languages = [language_filter]
                else:
                    languages = language_filter
                
                # Filter out 'all' if present
                languages = [lang.lower() for lang in languages if lang.lower() != 'all']
                
                if languages:
                    # Only add songs from the selected languages
                    language_mask = self.df['language'].str.lower().isin(languages)
                    available_songs = self.df[language_mask]
                else:
                    available_songs = self.df
            else:
                available_songs = self.df
            
            if len(available_songs) > 0:
                additional_songs = available_songs.sample(n=min(remaining, len(available_songs)))
                result = pd.concat([filtered_songs, additional_songs]).drop_duplicates()
                return result.head(n_songs)
            else:
                return filtered_songs
    
    def get_location_from_ip(self):
        """
        Get approximate location from IP address (fallback method)
        
        Returns:
            Dictionary with latitude and longitude
        """
        try:
            response = requests.get('https://ipapi.co/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'latitude': data.get('latitude', 0),
                    'longitude': data.get('longitude', 0),
                    'city': data.get('city', 'Unknown')
                }
        except:
            pass
        
        # Default location (New York)
        return {
            'latitude': 40.7128,
            'longitude': -74.0060,
            'city': 'New York'
        }
