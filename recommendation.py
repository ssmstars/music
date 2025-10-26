import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import warnings
warnings.filterwarnings('ignore')

class MusicRecommender:
    """
    Content-based music recommendation system using TF-IDF and cosine similarity
    """
    
    def __init__(self, df):
        """
        Initialize the recommender with a music dataset
        
        Args:
            df: Pandas DataFrame containing music data with columns like 
                'song', 'artist', 'genre', 'lyrics', 'mood', etc.
        """
        self.df = df.copy()
        self.similarity_matrix = None
        self.tfidf_vectorizer = None
        self._preprocess_data()
        self._build_recommendation_model()
    
    def _preprocess_data(self):
        """Preprocess the music data"""
        # Create a combined feature text from available columns
        feature_columns = []
        
        if 'lyrics' in self.df.columns:
            self.df['lyrics'] = self.df['lyrics'].fillna('')
            feature_columns.append('lyrics')
        
        if 'genre' in self.df.columns:
            self.df['genre'] = self.df['genre'].fillna('unknown')
            # Repeat genre to give it more weight
            feature_columns.append('genre')
            self.df['genre_weight'] = self.df['genre'] + ' ' + self.df['genre'] + ' ' + self.df['genre']
            feature_columns.append('genre_weight')
        
        if 'mood' in self.df.columns:
            self.df['mood'] = self.df['mood'].fillna('neutral')
            feature_columns.append('mood')
        
        if 'artist' in self.df.columns:
            self.df['artist'] = self.df['artist'].fillna('unknown')
            feature_columns.append('artist')
        
        # Combine all features into one text field
        if feature_columns:
            self.df['combined_features'] = self.df[feature_columns].apply(
                lambda x: ' '.join(x.astype(str)), axis=1
            )
        else:
            # Fallback if no feature columns found
            self.df['combined_features'] = self.df['song'].astype(str)
        
        # Clean up the text
        self.df['combined_features'] = self.df['combined_features'].str.lower()
    
    def _build_recommendation_model(self):
        """Build the TF-IDF model and compute similarity matrix"""
        # Create TF-IDF vectorizer
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        # Fit and transform the combined features
        tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['combined_features'])
        
        # Compute cosine similarity matrix
        self.similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        print(f"✓ Recommendation model built successfully!")
        print(f"  - Dataset size: {len(self.df)} songs")
        print(f"  - Feature matrix shape: {tfidf_matrix.shape}")
    
    def get_recommendations(self, song_name, n_recommendations=10, language_filter=None):
        """
        Get music recommendations based on a given song
        
        Args:
            song_name: Name of the song to base recommendations on
            n_recommendations: Number of recommendations to return
            language_filter: Optional language(s) to filter recommendations 
                           Can be a string, list of strings, or None
            
        Returns:
            DataFrame with recommended songs
        """
        try:
            # Find the song in the dataset
            song_indices = self.df[self.df['song'].str.lower() == song_name.lower()].index
            
            if len(song_indices) == 0:
                # Try partial match
                song_indices = self.df[self.df['song'].str.lower().str.contains(song_name.lower(), na=False)].index
                if len(song_indices) == 0:
                    print(f"Song '{song_name}' not found in database")
                    return None
            
            song_idx = song_indices[0]
            
            # Get similarity scores for this song
            similarity_scores = list(enumerate(self.similarity_matrix[song_idx]))
            
            # Sort by similarity score
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            
            # Filter by language if specified
            if language_filter and 'language' in self.df.columns:
                # Convert single language to list for uniform handling
                if isinstance(language_filter, str):
                    languages = [language_filter]
                else:
                    languages = language_filter
                
                # Filter out 'all' if present
                languages = [lang.lower() for lang in languages if lang.lower() != 'all']
                
                if languages:
                    # Get indices that match any of the language filters
                    language_mask = self.df['language'].str.lower().isin(languages)
                    valid_indices = set(self.df[language_mask].index.tolist())
                    
                    # Filter similarity scores to only include songs in the selected languages
                    filtered_scores = [(idx, score) for idx, score in similarity_scores 
                                     if idx in valid_indices and idx != song_idx]
                    
                    # Get top N recommendations from filtered results
                    top_indices = [i[0] for i in filtered_scores[:n_recommendations]]
                else:
                    # No valid language filter, get all
                    top_indices = [i[0] for i in similarity_scores[1:n_recommendations+1]]
            else:
                # Get top N recommendations (excluding the song itself)
                top_indices = [i[0] for i in similarity_scores[1:n_recommendations+1]]
            
            if not top_indices:
                print(f"No recommendations found for language filter: {language_filter}")
                return None
            
            # Return recommended songs
            recommendations = self.df.iloc[top_indices].copy()
            # Match similarity scores to the selected indices
            score_map = {idx: score for idx, score in similarity_scores}
            recommendations['similarity_score'] = [score_map[idx] for idx in top_indices]
            
            return recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return None
    
    def get_songs_by_mood(self, mood, n_songs=10):
        """
        Get songs filtered by mood
        
        Args:
            mood: The mood to filter by (e.g., 'happy', 'sad', 'energetic')
            n_songs: Number of songs to return
            
        Returns:
            DataFrame with songs matching the mood
        """
        if 'mood' not in self.df.columns:
            return self.df.head(n_songs)
        
        mood_songs = self.df[self.df['mood'].str.lower().str.contains(mood.lower(), na=False)]
        
        if len(mood_songs) == 0:
            return self.df.head(n_songs)
        
        return mood_songs.head(n_songs)
    
    def get_songs_by_genre(self, genre, n_songs=10):
        """
        Get songs filtered by genre
        
        Args:
            genre: The genre to filter by
            n_songs: Number of songs to return
            
        Returns:
            DataFrame with songs matching the genre
        """
        if 'genre' not in self.df.columns:
            return self.df.head(n_songs)
        
        genre_songs = self.df[self.df['genre'].str.lower().str.contains(genre.lower(), na=False)]
        
        if len(genre_songs) == 0:
            return self.df.head(n_songs)
        
        return genre_songs.head(n_songs)
    
    def get_random_songs(self, n_songs=10):
        """Get random songs from the dataset"""
        return self.df.sample(n=min(n_songs, len(self.df)))
    
    def get_available_languages(self):
        """
        Get list of available languages in the dataset
        
        Returns:
            List of unique languages
        """
        if 'language' not in self.df.columns:
            return []
        
        languages = self.df['language'].dropna().unique().tolist()
        return sorted(languages)
