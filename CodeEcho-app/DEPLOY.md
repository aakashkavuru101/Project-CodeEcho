# CodeEcho Application - Production Deployment

## Quick Deploy Options

### Option 1: Railway (Recommended - Free Tier Available)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Fork this repository
2. Connect your GitHub account to Railway
3. Import your forked repository
4. Set environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `PORT`: 5000 (auto-configured)
   - `FLASK_ENV`: production
5. Deploy automatically

### Option 2: Render (Free Tier)

1. Fork this repository
2. Create account on Render.com
3. Create new Web Service
4. Connect your repository
5. Set build command: `npm run deploy:build`
6. Set start command: `python backend/src/main.py`
7. Set environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `PORT`: 10000 (default for Render)
   - `FLASK_ENV`: production

### Option 3: Heroku

1. Install Heroku CLI
2. Fork this repository
3. Run deployment commands:
```bash
heroku create your-app-name
heroku config:set GEMINI_API_KEY=your-api-key-here
heroku config:set FLASK_ENV=production
git push heroku main
```

### Option 4: DigitalOcean App Platform

1. Fork this repository
2. Create DigitalOcean account
3. Use App Platform to deploy from GitHub
4. Configure build and run commands in app spec

## Environment Variables Required

- `GEMINI_API_KEY`: Your Google Gemini API key (required)
- `PORT`: Port number (default: 5000)
- `FLASK_ENV`: Set to "production" for production deployment
- `SECRET_KEY`: Flask secret key (optional, has secure default)

## Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key and set it as the `GEMINI_API_KEY` environment variable

## Local Development

1. Clone the repository
2. Run setup: `npm run setup`
3. Start backend: `npm run dev:backend`
4. Start frontend (separate terminal): `npm run dev:frontend`
5. Access at http://localhost:5173 (frontend) or http://localhost:5000 (production mode)

## Features

- **AI-Powered Analysis**: Uses Google Gemini to analyze websites
- **Responsive Design**: Built with React and Tailwind CSS
- **Production Ready**: Optimized for deployment on free hosting platforms
- **Fallback Support**: Works even when advanced browser automation fails
- **Environment Aware**: Automatically adapts to development/production environments

## Architecture

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: Flask + Python
- **AI**: Google Gemini API
- **Deployment**: Docker, Railway, Render, Heroku compatible