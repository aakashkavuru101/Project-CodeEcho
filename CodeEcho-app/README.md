# CodeEcho - AI-Powered Website Reverse Engineer

![CodeEcho Application](https://github.com/user-attachments/assets/f5869214-bcd9-4365-9506-1b4f35714d5f)

An intelligent web application that analyzes any website and generates comprehensive prompts for recreating similar applications using AI tools. **Now production-ready with free deployment options!**

## 🎯 Key Features

- **🔍 Smart Website Analysis**: Scrapes and analyzes website content, design, and functionality with fallback support
- **🤖 AI-Powered Prompt Generation**: Creates detailed prompts using Google Gemini API
- **📊 Multiple Output Formats**: Provides both human-readable text and structured JSON formats
- **📱 Responsive Modern UI**: Clean, mobile-friendly interface built with React and Tailwind CSS
- **⚡ Production Ready**: Optimized for deployment on free hosting platforms
- **🛡️ Robust Error Handling**: Works even when advanced browser automation fails

## 🌟 What You Get

- **🎨 Design Analysis**: Color palettes, typography, layout patterns
- **⚙️ Functionality Breakdown**: Features, interactions, user flows
- **🔧 Technical Recommendations**: Implementation strategies and best practices
- **📝 Content Strategy**: Guidelines for content creation and organization
- **👥 UX Guidelines**: User experience principles and accessibility considerations
- **🎯 Ready-to-use Prompts**: Formatted for use with ChatGPT, Claude, and other AI tools

## 🚀 Quick Deploy (Free Options)

### Railway (Recommended)
1. Fork this repository
2. Connect to [Railway](https://railway.app)
3. Ensure Ollama is set up (see setup instructions below)
4. Deploy automatically

### Render
1. Fork this repository  
2. Connect to [Render](https://render.com)
3. Use `deploy.sh` as build command
4. Set up Ollama on deployment environment

### Heroku
```bash
heroku create your-app-name
heroku config:set FLASK_ENV=production
git push heroku main
```

## 🤖 Ollama Setup

CodeEcho uses Ollama for secure, local AI inference with multiple open-source models.

### Quick Setup
1. Install Ollama: Visit [ollama.ai](https://ollama.ai)
2. Pull models:
```bash
ollama pull llama3.1:8b    # Primary: Fast & balanced
ollama pull qwen2.5:7b     # Reasoning & code
ollama pull mistral:7b     # Creative content  
ollama pull gemma2:9b      # Detailed analysis
```
3. Start service: `ollama serve`

## 💻 Technology Stack

### Backend
- **Flask**: Python web framework with production configuration
- **Ollama**: Local AI inference with multiple open-source models
- **BeautifulSoup + Requests**: Reliable web scraping with Playwright fallback
- **Robust Error Handling**: Works in any deployment environment

### Frontend
- **React**: Modern JavaScript framework
- **Tailwind CSS**: Utility-first CSS framework
- **Shadcn/UI**: High-quality UI components
- **Lucide Icons**: Beautiful icon library

### AI Models
- **Llama 3.1 8B**: Primary model for balanced performance
- **Qwen 2.5 7B**: Specialized for reasoning and code generation
- **Mistral 7B**: Optimized for creative content generation  
- **Gemma 2 9B**: Best for detailed, comprehensive analysis

## Installation & Setup

### Prerequisites
- Python 3.11+
- Node.js 20+
- npm or yarn
- Ollama installed and running

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

5. Set up environment variables:
```bash
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_API_BASE="https://api.manus.im/api/llm-proxy/v1"
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Build for production:
```bash
npm run build
```

4. Copy built files to Flask static directory:
```bash
cp -r dist/* ../backend/src/static/
```

## Running the Application

### Development Mode

1. Start the backend server:
```bash
cd backend
source venv/bin/activate
python src/main.py
```

2. In a separate terminal, start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Access the application:
- Frontend (development): http://localhost:5173
- Backend API: http://localhost:5000

### Production Mode

1. Build the frontend and copy to backend static directory (see Frontend Setup step 4)

2. Start the Flask server:
```bash
cd backend
source venv/bin/activate
python src/main.py
```

3. Access the application at http://localhost:5000

## API Endpoints

### POST /api/analyze-website
Analyzes a website and generates prompts.

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "status": "success",
  "session_id": "unique-session-id",
  "analysis": {
    "website_info": {...},
    "design_analysis": {...},
    "functionality_analysis": {...},
    "technical_analysis": {...},
    "summary": {...}
  },
  "prompts": {
    "text_preview": "...",
    "json_preview": {...}
  }
}
```

### GET /api/download/{session_id}
Downloads the complete analysis results as a ZIP file.

## Project Structure

```
reverse-engineer-app/
├── backend/
│   ├── src/
│   │   ├── main.py              # Flask application entry point
│   │   ├── routes/
│   │   │   ├── analyze.py       # Analysis API routes
│   │   │   └── user.py          # User management routes
│   │   ├── services/
│   │   │   ├── scraper.py       # Website scraping service
│   │   │   ├── analyzer.py      # Website analysis service
│   │   │   └── prompt_generator.py # AI prompt generation
│   │   ├── models/
│   │   │   └── user.py          # Database models
│   │   ├── static/              # Frontend build files
│   │   └── database/            # SQLite database
│   ├── venv/                    # Python virtual environment
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── main.jsx             # React entry point
│   │   └── components/          # UI components
│   ├── dist/                    # Built frontend files
│   ├── package.json             # Node.js dependencies
│   └── vite.config.js           # Vite configuration
└── README.md                    # This file
```

## Usage

1. **Enter Website URL**: Input the URL of the website you want to analyze
2. **Start Analysis**: Click the "Analyze" button to begin the reverse engineering process
3. **Review Results**: Explore the comprehensive analysis across different tabs:
   - Overview: Basic website information and statistics
   - Design: Color palettes, typography, and visual elements
   - Features: Functionality breakdown and user interactions
   - Technical: Implementation details and technologies used
   - Prompts: Generated AI prompts for recreation
4. **Download Results**: Click "Download Results" to get a ZIP file containing all analysis data

## Output Formats

### Text Format
Human-readable prompts optimized for AI tools like ChatGPT, Claude, or other language models.

### JSON Format
Structured data format containing:
- Complete analysis breakdown
- Categorized requirements
- Technical specifications
- Design guidelines
- Implementation recommendations

## Limitations

- Analysis quality depends on website accessibility and structure
- Some dynamic content may not be fully captured
- JavaScript-heavy applications may require additional analysis
- Rate limiting may apply for frequent requests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues, questions, or contributions, please open an issue on the project repository.

## Acknowledgments

- OpenAI for providing the AI capabilities
- Playwright team for the excellent web automation tools
- React and Tailwind CSS communities for the frontend technologies
- Shadcn/UI for the beautiful component library

