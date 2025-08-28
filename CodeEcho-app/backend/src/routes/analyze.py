"""
API routes for website analysis and prompt generation.
"""
import asyncio
import json
import os
import uuid
from datetime import datetime
from flask import Blueprint, request, jsonify, send_file
from werkzeug.exceptions import BadRequest
import tempfile
import zipfile
import logging

from src.services.scraper import scrape_website_sync
from src.services.analyzer import WebsiteAnalyzer
from src.services.prompt_generator import PromptGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

analyze_bp = Blueprint('analyze', __name__)

# Store analysis results temporarily (in production, use a database)
analysis_cache = {}

@analyze_bp.route('/analyze-website', methods=['POST'])
def analyze_website():
    """
    Analyze a website and generate prompts for recreation.
    
    Expected JSON payload:
    {
        "url": "https://example.com"
    }
    
    Returns:
    {
        "session_id": "unique_session_id",
        "status": "success",
        "analysis": {...},
        "prompts": {...}
    }
    """
    try:
        # Validate request
        if not request.is_json:
            raise BadRequest("Request must be JSON")
        
        data = request.get_json()
        url = data.get('url')
        
        if not url:
            raise BadRequest("URL is required")
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        logger.info(f"Starting analysis for URL: {url}")
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Step 1: Scrape the website
        logger.info("Step 1: Scraping website...")
        try:
            scraped_data = scrape_website_sync(url)
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to scrape website: {str(e)}',
                'error_type': 'scraping_error'
            }), 400
        
        # Step 2: Analyze the scraped data
        logger.info("Step 2: Analyzing scraped data...")
        try:
            analyzer = WebsiteAnalyzer()
            analysis_result = analyzer.analyze_scraped_data(scraped_data)
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to analyze website: {str(e)}',
                'error_type': 'analysis_error'
            }), 500
        
        # Step 3: Generate prompts
        logger.info("Step 3: Generating prompts...")
        try:
            prompt_generator = PromptGenerator()
            prompt_result = prompt_generator.generate_comprehensive_prompt(analysis_result)
        except Exception as e:
            logger.error(f"Prompt generation failed: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to generate prompts: {str(e)}',
                'error_type': 'prompt_generation_error'
            }), 500
        
        # Store results in cache
        analysis_cache[session_id] = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'scraped_data': scraped_data,
            'analysis_result': analysis_result,
            'prompt_result': prompt_result
        }
        
        logger.info(f"Analysis completed successfully for session: {session_id}")
        
        # Return response
        return jsonify({
            'session_id': session_id,
            'status': 'success',
            'analysis': {
                'website_info': analysis_result.get('website_info', {}),
                'design_analysis': analysis_result.get('design_analysis', {}),
                'functionality_analysis': analysis_result.get('functionality_analysis', {}),
                'technical_analysis': analysis_result.get('technical_analysis', {}),
                'summary': {
                    'website_type': analysis_result.get('website_info', {}).get('website_type', ''),
                    'primary_purpose': analysis_result.get('website_info', {}).get('primary_purpose', ''),
                    'business_type': analysis_result.get('business_model', {}).get('business_type', ''),
                    'core_features': analysis_result.get('functionality_analysis', {}).get('core_features', [])
                }
            },
            'prompts': {
                'text_preview': prompt_result.get('text_format', '')[:1000] + '...' if len(prompt_result.get('text_format', '')) > 1000 else prompt_result.get('text_format', ''),
                'json_preview': {
                    'project_overview': prompt_result.get('json_format', {}).get('project_overview', {}),
                    'requirements_summary': {
                        'design': len(prompt_result.get('sections', {}).get('design', '')),
                        'functionality': len(prompt_result.get('sections', {}).get('functionality', '')),
                        'technical': len(prompt_result.get('sections', {}).get('technical', '')),
                        'content': len(prompt_result.get('sections', {}).get('content', '')),
                        'user_experience': len(prompt_result.get('sections', {}).get('user_experience', ''))
                    }
                },
                'metadata': prompt_result.get('metadata', {})
            }
        })
        
    except BadRequest as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'error_type': 'validation_error'
        }), 400
    except Exception as e:
        logger.error(f"Unexpected error in analyze_website: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred during analysis',
            'error_type': 'internal_error'
        }), 500

@analyze_bp.route('/download/<session_id>', methods=['GET'])
def download_results(session_id):
    """
    Download analysis results as a zip file.
    
    Args:
        session_id: The session ID from the analysis
        
    Returns:
        ZIP file containing:
        - prompt.txt (text format prompt)
        - prompt.json (JSON format prompt)
        - analysis.json (full analysis data)
        - metadata.json (session metadata)
    """
    try:
        # Check if session exists
        if session_id not in analysis_cache:
            return jsonify({
                'status': 'error',
                'message': 'Session not found or expired',
                'error_type': 'session_not_found'
            }), 404
        
        session_data = analysis_cache[session_id]
        
        # Create temporary directory for files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create files
            files_created = []
            
            # 1. Text prompt file
            text_prompt_path = os.path.join(temp_dir, 'prompt.txt')
            with open(text_prompt_path, 'w', encoding='utf-8') as f:
                f.write(session_data['prompt_result']['text_format'])
            files_created.append(('prompt.txt', text_prompt_path))
            
            # 2. JSON prompt file
            json_prompt_path = os.path.join(temp_dir, 'prompt.json')
            with open(json_prompt_path, 'w', encoding='utf-8') as f:
                json.dump(session_data['prompt_result']['json_format'], f, indent=2, ensure_ascii=False)
            files_created.append(('prompt.json', json_prompt_path))
            
            # 3. Full analysis data
            analysis_path = os.path.join(temp_dir, 'analysis.json')
            with open(analysis_path, 'w', encoding='utf-8') as f:
                json.dump(session_data['analysis_result'], f, indent=2, ensure_ascii=False)
            files_created.append(('analysis.json', analysis_path))
            
            # 4. Session metadata
            metadata_path = os.path.join(temp_dir, 'metadata.json')
            metadata = {
                'session_id': session_id,
                'url': session_data['url'],
                'timestamp': session_data['timestamp'],
                'tool_version': '1.0.0',
                'files_included': [filename for filename, _ in files_created]
            }
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            files_created.append(('metadata.json', metadata_path))
            
            # 5. README file
            readme_path = os.path.join(temp_dir, 'README.md')
            readme_content = f"""# Website Reverse Engineering Results

## Overview
This package contains the reverse engineering analysis and prompts for:
**URL:** {session_data['url']}
**Analysis Date:** {session_data['timestamp']}
**Session ID:** {session_id}

## Files Included

### prompt.txt
Human-readable prompt for recreating a similar website/application. This file contains comprehensive instructions covering design, functionality, technical implementation, content strategy, and user experience guidelines.

### prompt.json
Structured JSON format of the same prompt, suitable for programmatic processing or integration with other tools.

### analysis.json
Complete analysis data including:
- Website information and classification
- Design analysis (colors, typography, layout)
- Functionality analysis (features, interactions, navigation)
- Technical analysis (technologies, performance, security)
- Content strategy analysis
- User experience analysis
- Business model insights

### metadata.json
Session metadata and file information.

## Usage Instructions

1. **For AI/LLM Prompting:** Use `prompt.txt` or `prompt.json` as input to your preferred AI model
2. **For Development Planning:** Review `analysis.json` for detailed technical specifications
3. **For Project Management:** Use the structured data to create development tasks and timelines

## Important Notes

- This analysis is generated automatically and may require human review and validation
- Adapt the prompts based on your specific requirements and constraints
- Consider conducting user research to validate assumptions about target audience and use cases
- Ensure compliance with accessibility standards and legal requirements in your implementation

## Tool Information

Generated by: Website Reverse Engineering Tool v1.0.0
Analysis Engine: Automated web scraping and AI-powered analysis
Prompt Generation: OpenAI GPT-4 powered prompt engineering

---
For questions or support, please refer to the tool documentation.
"""
            with open(readme_path, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            files_created.append(('README.md', readme_path))
            
            # Create ZIP file
            zip_path = os.path.join(temp_dir, f'website_analysis_{session_id[:8]}.zip')
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for filename, filepath in files_created:
                    zipf.write(filepath, filename)
            
            logger.info(f"Created download package for session: {session_id}")
            
            # Send file
            return send_file(
                zip_path,
                as_attachment=True,
                download_name=f'website_analysis_{session_id[:8]}.zip',
                mimetype='application/zip'
            )
    
    except Exception as e:
        logger.error(f"Error creating download package: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to create download package',
            'error_type': 'download_error'
        }), 500

@analyze_bp.route('/session/<session_id>', methods=['GET'])
def get_session_data(session_id):
    """
    Get full session data for a given session ID.
    
    Args:
        session_id: The session ID from the analysis
        
    Returns:
        Complete session data including analysis and prompts
    """
    try:
        if session_id not in analysis_cache:
            return jsonify({
                'status': 'error',
                'message': 'Session not found or expired',
                'error_type': 'session_not_found'
            }), 404
        
        session_data = analysis_cache[session_id]
        
        return jsonify({
            'status': 'success',
            'session_id': session_id,
            'url': session_data['url'],
            'timestamp': session_data['timestamp'],
            'analysis': session_data['analysis_result'],
            'prompts': session_data['prompt_result']
        })
        
    except Exception as e:
        logger.error(f"Error retrieving session data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve session data',
            'error_type': 'retrieval_error'
        }), 500

@analyze_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'website-reverse-engineering',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@analyze_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'error_type': 'not_found'
    }), 404

@analyze_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'error_type': 'internal_error'
    }), 500

