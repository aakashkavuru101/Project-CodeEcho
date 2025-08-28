#!/bin/bash

# CodeEcho Deployment Script
echo "🚀 Starting CodeEcho deployment build..."

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt

# Go back to root
cd ..

# Install frontend dependencies  
echo "📦 Installing frontend dependencies..."
cd frontend
npm install --legacy-peer-deps

# Build frontend
echo "🔨 Building frontend..."
npm run build

# Copy to backend static directory
echo "📋 Copying frontend build to backend..."
cp -r dist/* ../backend/src/static/

# Go back to root
cd ..

echo "✅ Build complete! Ready for deployment."
echo ""
echo "🌐 To deploy to different platforms:"
echo "   Railway: Push to GitHub and connect via Railway dashboard"
echo "   Render: Push to GitHub and connect via Render dashboard"  
echo "   Heroku: heroku create app-name && git push heroku main"
echo ""
echo "🔑 Remember to set GEMINI_API_KEY environment variable!"
echo "   Get your key from: https://makersuite.google.com/app/apikey"