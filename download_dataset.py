"""
Download and prepare Spotify Million Song Dataset from Kaggle
"""
import kagglehub
import pandas as pd
import os

def download_spotify_dataset():
    """Download the Spotify Million Song Dataset from Kaggle"""
    print("=" * 60)
    print("📥 Downloading Spotify Million Song Dataset from Kaggle...")
    print("=" * 60)
    
    try:
        # Download latest version of the dataset
        path = kagglehub.dataset_download("notshrirang/spotify-million-song-dataset")
        
        print(f"✓ Dataset downloaded successfully!")
        print(f"📁 Path to dataset files: {path}")
        
        # List all files in the downloaded dataset
        files = os.listdir(path)
        print(f"\n📄 Available files: {files}")
        
        # Load the dataset
        csv_file = None
        for file in files:
            if file.endswith('.csv'):
                csv_file = file
                break
        
        if csv_file:
            print(f"\n📊 Loading dataset from: {csv_file}")
            df = pd.read_csv(os.path.join(path, csv_file))
            
            print(f"\n✓ Dataset loaded successfully!")
            print(f"   - Total songs: {len(df):,}")
            print(f"   - Columns: {list(df.columns)}")
            print(f"   - Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            print(f"\n📊 First 5 records:")
            print(df.head())
            
            print(f"\n📊 Dataset Info:")
            print(df.info())
            
            # Save to data folder
            output_path = 'data/spotify_million_songs.csv'
            os.makedirs('data', exist_ok=True)
            
            # Check if we need to preprocess
            print(f"\n🔄 Preprocessing dataset...")
            
            # For recommendation system, we need: song name, artist, and text features
            # Let's check what columns are available
            print(f"\nAvailable columns: {df.columns.tolist()}")
            
            # Save the preprocessed dataset
            df.to_csv(output_path, index=False)
            print(f"\n✓ Dataset saved to: {output_path}")
            
            return df, output_path
        else:
            print("❌ No CSV file found in the dataset!")
            return None, None
            
    except Exception as e:
        print(f"❌ Error downloading dataset: {e}")
        print("\nNote: You might need to authenticate with Kaggle.")
        print("Please set up your Kaggle API credentials:")
        print("1. Go to https://www.kaggle.com/settings")
        print("2. Scroll to 'API' section and click 'Create New Token'")
        print("3. Place kaggle.json in: ~/.kaggle/ (Linux/Mac) or C:\\Users\\<username>\\.kaggle\\ (Windows)")
        return None, None

if __name__ == "__main__":
    df, path = download_spotify_dataset()
    
    if df is not None:
        print("\n" + "=" * 60)
        print("✅ Dataset ready for use!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("⚠️  Using existing music_data.csv as fallback")
        print("=" * 60)
