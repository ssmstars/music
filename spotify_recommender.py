import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class SpotifyMusicRecommender:
    """
    Content-based music recommendation system using TF-IDF and cosine similarity
    Optimized for Spotify Million Song Dataset
    """
    
    def __init__(self, df):
        """
        Initialize the recommender with Spotify music dataset
        
        Args:
            df: Pandas DataFrame containing music data with columns:
                'song', 'artist', 'text' (lyrics), 'link'
        """
        self.df = df.copy()
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.tfidf_vectorizer = None
        self._preprocess_data()
        self._build_recommendation_model()
    
    def _preprocess_data(self):
        """Preprocess the Spotify music data"""
        # Clean and prepare data
        self.df['song'] = self.df['song'].fillna('Unknown')
        self.df['artist'] = self.df['artist'].fillna('Unknown')
        self.df['text'] = self.df['text'].fillna('')
        
        # Create combined features with weighted importance
        # Artist (repeated 3x for more weight) + Song + Lyrics
        self.df['combined_features'] = (
            self.df['artist'].astype(str) + ' ' +
            self.df['artist'].astype(str) + ' ' +
            self.df['artist'].astype(str) + ' ' +
            self.df['song'].astype(str) + ' ' +
            self.df['text'].astype(str)
        )
        
        # Clean up the text
        self.df['combined_features'] = self.df['combined_features'].str.lower()
        
        # Remove duplicates based on song and artist
        self.df = self.df.drop_duplicates(subset=['song', 'artist'], keep='first')
        self.df = self.df.reset_index(drop=True)
    
    def _build_recommendation_model(self):
        """Build the TF-IDF model (similarity computed on-demand)"""
        # Create TF-IDF vectorizer with optimized parameters for fast loading
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,  # Reduced for faster computation
            stop_words='english',
            ngram_range=(1, 2),
            min_df=3,  # Ignore terms that appear in less than 3 documents
            max_df=0.7  # Ignore terms that appear in more than 70% of documents
        )
        
        # Fit and transform the combined features
        print(f"🔄 Building TF-IDF matrix for {len(self.df):,} songs...")
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.df['combined_features'])
        
        # Don't pre-compute full similarity matrix for large datasets
        # Instead, compute similarities on-demand
        self.similarity_matrix = None
        
        print(f"✓ Recommendation model built successfully!")
        print(f"  - Dataset size: {len(self.df):,} songs")
        print(f"  - Feature matrix shape: {self.tfidf_matrix.shape}")
        print(f"  - Unique artists: {self.df['artist'].nunique():,}")
        print(f"  - Using on-demand similarity computation for efficiency")
    
    def get_recommendations(self, song_name, n_recommendations=10, language_filter=None):
        """
        Get music recommendations based on a given song
        
        Args:
            song_name: Name of the song to base recommendations on
            n_recommendations: Number of recommendations to return
            language_filter: Optional language to filter recommendations (compatibility with MusicRecommender)
            
        Returns:
            DataFrame with recommended songs
        """
        try:
            # Find the song in the dataset (exact match first)
            song_indices = self.df[self.df['song'].str.lower() == song_name.lower()].index
            
            if len(song_indices) == 0:
                # Try partial match
                song_indices = self.df[self.df['song'].str.lower().str.contains(song_name.lower(), na=False)].index
                
                if len(song_indices) == 0:
                    return None
            
            # Get the first matching song index
            song_idx = song_indices[0]
            
            # Compute similarity for this song only (on-demand)
            song_vector = self.tfidf_matrix[song_idx]
            similarity_scores = cosine_similarity(song_vector, self.tfidf_matrix).flatten()
            
            # Get indices of most similar songs
            similar_indices = similarity_scores.argsort()[::-1]
            
            # Filter by language if applicable and column exists
            if language_filter and language_filter.lower() != 'all' and 'language' in self.df.columns:
                language_mask = self.df['language'].str.lower() == language_filter.lower()
                valid_indices = set(self.df[language_mask].index.tolist())
                
                # Filter similar indices to only include songs in the selected language
                filtered_indices = [i for i in similar_indices if i in valid_indices and i != song_idx]
                top_indices = filtered_indices[:n_recommendations]
            else:
                # Get top N similar songs (excluding the input song itself)
                top_indices = [i for i in similar_indices if i != song_idx][:n_recommendations]
            
            if not top_indices:
                return None
            
            # Return recommended songs
            recommendations = self.df.iloc[top_indices][['song', 'artist', 'link']].copy()
            recommendations['similarity_score'] = similarity_scores[top_indices]
            
            return recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def get_random_songs(self, n=50):
        """Get random songs from the dataset"""
        return self.df[['song', 'artist']].sample(n=min(n, len(self.df)))
    
    def search_songs(self, query, limit=50):
        """
        Search for songs by name or artist
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            DataFrame with matching songs
        """
        query_lower = query.lower()
        
        # Search in both song names and artists
        mask = (
            self.df['song'].str.lower().str.contains(query_lower, na=False) |
            self.df['artist'].str.lower().str.contains(query_lower, na=False)
        )
        
        results = self.df[mask][['song', 'artist', 'link']].head(limit)
        return results
    
    def get_songs_by_artist(self, artist_name, limit=20):
        """Get all songs by a specific artist"""
        mask = self.df['artist'].str.lower().str.contains(artist_name.lower(), na=False)
        return self.df[mask][['song', 'artist', 'link']].head(limit)
    
    def get_available_languages(self):
        """
        Get list of available languages in the dataset (compatibility method)
        
        Returns:
            List of unique languages
        """
        if 'language' not in self.df.columns:
            return []
        
        languages = self.df['language'].dropna().unique().tolist()
        return sorted(languages)
