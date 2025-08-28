# CodeEcho Application - Production Deployment

## Quick Deploy Options

### Option 1: Railway (Recommended - Free Tier Available)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

1. Fork this repository
2. Connect your GitHub account to Railway
3. Import your forked repository
4. Set environment variables:
   - `PORT`: 5000 (auto-configured)
   - `FLASK_ENV`: production
   - `OLLAMA_BASE_URL`: Set if using remote Ollama instance
5. Ensure Ollama is available (see Ollama Setup section)
6. Deploy automatically

### Option 2: Render (Free Tier)

1. Fork this repository
2. Create account on Render.com
3. Create new Web Service
4. Connect your repository
5. Set build command: `npm run deploy:build`
6. Set start command: `python backend/src/main.py`
7. Set environment variables:
   - `PORT`: 10000 (default for Render)
   - `FLASK_ENV`: production
   - `OLLAMA_BASE_URL`: Set if using remote Ollama instance

### Option 3: Heroku

1. Install Heroku CLI
2. Fork this repository
3. Run deployment commands:
```bash
heroku create your-app-name
heroku config:set FLASK_ENV=production
git push heroku main
```

### Option 4: DigitalOcean App Platform

1. Fork this repository
2. Create DigitalOcean account
3. Use App Platform to deploy from GitHub
4. Configure build and run commands in app spec

## Environment Variables Required

- `PORT`: Port number (default: 5000)
- `FLASK_ENV`: Set to "production" for production deployment
- `SECRET_KEY`: Flask secret key (optional, has secure default)
- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)

## Ollama Setup

CodeEcho now uses Ollama for secure, local AI model inference instead of external APIs.

### Local Development

1. Install Ollama: Visit [ollama.ai](https://ollama.ai) and download for your OS
2. Pull required models:
```bash
ollama pull llama3.1:8b
ollama pull qwen2.5:7b  
ollama pull mistral:7b
ollama pull gemma2:9b
```
3. Start Ollama service: `ollama serve`

### Production Deployment

For production environments, ensure Ollama is installed and the required models are available:

```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull models
ollama pull llama3.1:8b
ollama pull qwen2.5:7b
ollama pull mistral:7b  
ollama pull gemma2:9b

# Start service
ollama serve
```

## Local Development

1. Clone the repository
2. Install Ollama and required models (see Ollama Setup)
3. Run setup: `npm run setup`
4. Start backend: `npm run dev:backend`
5. Start frontend (separate terminal): `npm run dev:frontend`
6. Access at http://localhost:5173 (frontend) or http://localhost:5000 (production mode)

## Features

- **AI-Powered Analysis**: Uses Ollama with multiple open-source models
- **Responsive Design**: Built with React and Tailwind CSS
- **Production Ready**: Optimized for deployment on free hosting platforms
- **Fallback Support**: Works even when advanced browser automation fails
- **Environment Aware**: Automatically adapts to development/production environments
- **Model Redundancy**: 4 models with automatic fallback for reliability

## Architecture

- **Frontend**: React + Vite + Tailwind CSS
- **Backend**: Flask + Python
- **AI**: Ollama with multiple open-source models (Llama, Qwen, Mistral, Gemma)
- **Deployment**: Docker, Railway, Render, Heroku compatible