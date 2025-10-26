"""
Alternative entry point for Vercel deployment
This file ensures compatibility with Vercel's serverless functions
"""
from app import app

# Export the Flask app for Vercel
# Vercel will use this as the WSGI application
application = app

# Also support 'app' export
__all__ = ['app', 'application']
