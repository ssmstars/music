# 🚀 Vercel Deployment Guide for Dynamic Tune

## Overview
This guide will help you deploy Dynamic Tune to Vercel successfully.

## Important Notes

### Dataset Limitations
⚠️ **Vercel Limitations:**
- Max deployment size: ~100MB
- Function timeout: 10 seconds (Hobby plan) / 60 seconds (Pro plan)
- The Spotify Million Song Dataset (82MB) is **excluded** from Vercel deployment

The app will automatically use the fallback dataset (`data/music_data.csv` - 84 songs) on Vercel, which is perfect for demo purposes.

## Deployment Steps

### 1. Prerequisites
- GitHub account
- Vercel account (free tier works fine)
- Your repository pushed to GitHub

### 2. Prepare for Deployment

Make sure you have these files in your repository:
- ✅ `vercel.json` - Vercel configuration
- ✅ `wsgi.py` - WSGI entry point
- ✅ `runtime.txt` - Python version
- ✅ `.vercelignore` - Excludes large files
- ✅ `requirements.txt` - Python dependencies
- ✅ `data/music_data.csv` - Fallback dataset (84 songs)

### 3. Deploy to Vercel

#### Option A: Deploy via Vercel Dashboard (Recommended)
1. Go to [vercel.com](https://vercel.com) and sign in
2. Click "Add New Project"
3. Import your GitHub repository: `hvkr15/AI-and-weather-Based-Music-Recommendation-System---Mini-Project`
4. Vercel will auto-detect Flask app
5. **Environment Variables** (Optional):
   - Add any API keys if needed
   - Example: `OPENWEATHER_API_KEY=your_key_here`
6. Click "Deploy"
7. Wait 2-3 minutes for deployment

#### Option B: Deploy via Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Login to Vercel
vercel login

# Deploy (from project directory)
cd "d:\Mini Project 5th sem"
vercel

# Follow the prompts:
# - Set up and deploy? Yes
# - Which scope? (Your account)
# - Link to existing project? No
# - Project name? dynamic-tune (or your choice)
# - Directory? ./
# - Override settings? No

# Deploy to production
vercel --prod
```

### 4. Post-Deployment

After successful deployment, you'll get a URL like:
```
https://dynamic-tune-xxxxxx.vercel.app
```

**Test these endpoints:**
- ✅ Homepage: `https://your-app.vercel.app/`
- ✅ Lyrics Generator: `https://your-app.vercel.app/lyrics-generator`
- ✅ Song Generator: `https://your-app.vercel.app/song-generator`
- ✅ API: Test music recommendations

## Troubleshooting

### Issue: 404 Error
**Cause:** Missing `vercel.json` or incorrect routes configuration
**Solution:** ✅ Already fixed with the `vercel.json` file

### Issue: 500 Internal Server Error
**Cause:** Missing dependencies or dataset
**Solution:** 
- Check Vercel logs: `vercel logs`
- Ensure `data/music_data.csv` exists in repo
- Verify all requirements are in `requirements.txt`

### Issue: Function Timeout
**Cause:** Large dataset causing slow initialization
**Solution:** ✅ Already handled - uses fallback dataset on Vercel

### Issue: Module Not Found
**Cause:** Missing package in `requirements.txt`
**Solution:** 
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
# Redeploy on Vercel
```

### Issue: Static Files Not Loading
**Cause:** Incorrect static file routing
**Solution:** ✅ Already configured in `vercel.json`

## Configuration Files Explained

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```
- **builds**: Tells Vercel to build Python app
- **routes**: Maps URLs to Flask app and static files

### wsgi.py
```python
from app import app
```
- Imports Flask app for serverless execution

### runtime.txt
```
python-3.9
```
- Specifies Python version for Vercel

## Performance on Vercel

### Expected Performance:
- **Load Time**: 2-3 seconds (first request)
- **Subsequent Requests**: <1 second
- **Dataset**: 84 songs (fallback)
- **Concurrent Users**: ~10-50 (Hobby plan)

### Scaling Options:
- **Hobby Plan** (Free): Perfect for demos and projects
- **Pro Plan** ($20/month): More concurrent users, longer timeouts
- **Enterprise**: Custom limits

## Local vs Vercel

| Feature | Local Development | Vercel Deployment |
|---------|------------------|-------------------|
| Dataset | 57,650 songs (82MB) | 84 songs (50KB) |
| Startup | 10-15 seconds | 2-3 seconds |
| Performance | Full ML power | Optimized for demo |
| Cost | Free | Free (Hobby) |

## Custom Domain (Optional)

1. In Vercel Dashboard, go to your project
2. Click "Settings" → "Domains"
3. Add your custom domain
4. Update DNS settings as instructed
5. Wait for DNS propagation (5-30 minutes)

Example: `dynamictune.com` → `dynamic-tune.vercel.app`

## Continuous Deployment

Once connected to GitHub:
- Any push to `main` branch → Auto-deploys to production
- Pull requests → Deploy previews
- Rollback available in Vercel dashboard

## Monitoring

### View Logs:
```bash
vercel logs [deployment-url]
```

### Check Deployment Status:
```bash
vercel ls
```

### Inspect Build:
```bash
vercel inspect [deployment-url]
```

## Environment Variables

If you need to add API keys:

1. Vercel Dashboard → Project → Settings → Environment Variables
2. Add variables:
   - `OPENWEATHER_API_KEY` = your key
   - `SECRET_KEY` = your secret key
3. Redeploy

## Best Practices

1. ✅ Keep deployment size under 100MB
2. ✅ Use `.vercelignore` to exclude unnecessary files
3. ✅ Test locally before deploying
4. ✅ Monitor logs after deployment
5. ✅ Use environment variables for secrets
6. ✅ Enable automatic deployments from GitHub

## Getting Help

- **Vercel Docs**: https://vercel.com/docs
- **Vercel Discord**: https://vercel.com/discord
- **GitHub Issues**: Create an issue in your repo

## Summary

Your Dynamic Tune app is now configured for Vercel deployment! 🎉

**Quick Deploy:**
1. Push to GitHub
2. Connect to Vercel
3. Deploy
4. Share your URL!

**Your deployment will work perfectly with the fallback dataset for demo purposes.**

---

Made with ❤️ for Dynamic Tune - 5th Sem AIML Project
