"""
WSGI entry point for Vercel deployment
"""
from app import app

# Vercel needs the Flask app instance
if __name__ == "__main__":
    app.run()
