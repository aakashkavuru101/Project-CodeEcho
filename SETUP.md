# CodeEcho Project Setup Guide

## Quick Start (After Cloning or Reopening)

### 1. Activate Virtual Environment
```powershell
# Navigate to project root
cd d:\GitHub\Project-CodeEcho

# Activate the virtual environment
.venv\Scripts\activate
```

### 2. Start Backend Server
```powershell
cd CodeEcho-app\backend\src
python main.py
```
Backend will be available at: http://127.0.0.1:5000

### 3. Start Frontend Server (New Terminal)
```powershell
cd CodeEcho-app\frontend
npm run dev
```
Frontend will be available at: http://localhost:5173

## First Time Setup (Only if .venv doesn't exist)

If the virtual environment gets deleted or corrupted:

```powershell
# Create new virtual environment
python -m venv .venv

# Activate it
.venv\Scripts\activate

# Install Python dependencies
cd CodeEcho-app\backend
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install frontend dependencies (if needed)
cd ..\frontend
npm install --legacy-peer-deps
```

## Troubleshooting

### "Flask not found" or similar errors
- Make sure virtual environment is activated (you should see `(.venv)` in your terminal prompt)
- If still issues, recreate the virtual environment using the "First Time Setup" steps above

### Frontend issues
- Run `npm install --legacy-peer-deps` in the frontend directory

### Ollama models not found
- The application will automatically attempt to download required models on first use
- Make sure Ollama is installed on your system

## Project Structure
- `CodeEcho-app/backend/` - Flask API server
- `CodeEcho-app/frontend/` - React frontend
- `.venv/` - Python virtual environment (local, not in git)
