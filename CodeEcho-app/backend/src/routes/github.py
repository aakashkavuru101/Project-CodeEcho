"""
API routes for GitHub repository analysis and portfolio website generation.
"""
import asyncio
import json
import os
import uuid
import logging
from datetime import datetime
from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest

from src.services.github_analyzer import GitHubAnalyzer
from src.services.website_generator import WebsiteTemplateGenerator
from src.services.cache_service import CacheService, FallbackCache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

github_bp = Blueprint('github', __name__)

# Initialize services
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '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')

# Try MongoDB cache first, fallback to in-memory cache
try:
    cache_service = CacheService()
    if not cache_service.connected:
        cache_service = FallbackCache()
        logger.info("Using fallback in-memory cache")
except Exception as e:
    logger.warning(f"Failed to initialize cache service: {e}")
    cache_service = FallbackCache()
    logger.info("Using fallback in-memory cache")

github_analyzer = GitHubAnalyzer(github_token=GITHUB_TOKEN)
website_generator = WebsiteTemplateGenerator()

# Store analysis results temporarily (in production, use a database)
analysis_cache = {}

@github_bp.route('/analyze-repository', methods=['POST'])
def analyze_repository():
    """
    Analyze a GitHub repository and generate a portfolio website.
    
    Expected JSON payload:
    {
        "url": "https://github.com/owner/repo"
    }
    
    Returns:
    {
        "session_id": "unique_session_id",
        "status": "success",
        "analysis": {...},
        "website": {...}
    }
    """
    try:
        # Validate request
        if not request.is_json:
            raise BadRequest("Request must be JSON")
        
        data = request.get_json()
        github_url = data.get('url')
        
        if not github_url:
            raise BadRequest("GitHub URL is required")
        
        # Validate GitHub URL format
        if 'github.com' not in github_url.lower():
            raise BadRequest("Please provide a valid GitHub repository URL")
        
        logger.info(f"Starting GitHub repository analysis for: {github_url}")
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Check cache first
        cached_analysis = cache_service.get(github_url)
        if cached_analysis:
            logger.info(f"Using cached analysis for: {github_url}")
            
            # Generate fresh website from cached analysis
            website_result = website_generator.generate_website(cached_analysis)
            
            # Store in session cache
            analysis_cache[session_id] = {
                'url': github_url,
                'timestamp': datetime.now().isoformat(),
                'analysis_result': cached_analysis,
                'website_result': website_result,
                'from_cache': True
            }
            
            return jsonify({
                'session_id': session_id,
                'status': 'success',
                'from_cache': True,
                'analysis': {
                    'repository_info': cached_analysis.get('repository_info', {}),
                    'tech_stack': cached_analysis.get('tech_stack', {}),
                    'project_analysis': cached_analysis.get('project_analysis', {}),
                    'website_generation': cached_analysis.get('website_generation', {}),
                    'readme_analysis': cached_analysis.get('readme_analysis', {})
                },
                'website': {
                    'preview_url': f'/api/website-preview/{session_id}',
                    'template_type': website_result['metadata']['template_type'],
                    'color_scheme': website_result['metadata']['color_scheme'],
                    'generated_at': website_result['metadata']['generated_at']
                }
            })
        
        # Step 1: Analyze the GitHub repository
        logger.info("Step 1: Analyzing GitHub repository...")
        try:
            analysis_result = github_analyzer.analyze_repository(github_url)
        except Exception as e:
            logger.error(f"GitHub analysis failed: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to analyze GitHub repository: {str(e)}',
                'error_type': 'github_analysis_error'
            }), 500
        
        # Step 2: Generate portfolio website
        logger.info("Step 2: Generating portfolio website...")
        try:
            website_result = website_generator.generate_website(analysis_result)
        except Exception as e:
            logger.error(f"Website generation failed: {str(e)}")
            return jsonify({
                'status': 'error',
                'message': f'Failed to generate website: {str(e)}',
                'error_type': 'website_generation_error'
            }), 500
        
        # Step 3: Cache the analysis result
        logger.info("Step 3: Caching analysis result...")
        try:
            cache_service.set(github_url, analysis_result, ttl_hours=24)
        except Exception as e:
            logger.warning(f"Failed to cache analysis result: {str(e)}")
        
        # Store results in session cache
        analysis_cache[session_id] = {
            'url': github_url,
            'timestamp': datetime.now().isoformat(),
            'analysis_result': analysis_result,
            'website_result': website_result,
            'from_cache': False
        }
        
        logger.info(f"Repository analysis completed successfully for session: {session_id}")
        
        # Return response
        return jsonify({
            'session_id': session_id,
            'status': 'success',
            'from_cache': False,
            'analysis': {
                'repository_info': analysis_result.get('repository_info', {}),
                'tech_stack': analysis_result.get('tech_stack', {}),
                'project_analysis': analysis_result.get('project_analysis', {}),
                'website_generation': analysis_result.get('website_generation', {}),
                'readme_analysis': analysis_result.get('readme_analysis', {})
            },
            'website': {
                'preview_url': f'/api/website-preview/{session_id}',
                'template_type': website_result['metadata']['template_type'],
                'color_scheme': website_result['metadata']['color_scheme'],
                'generated_at': website_result['metadata']['generated_at']
            }
        })
        
    except BadRequest as e:
        return jsonify({
            'status': 'error',
            'message': str(e),
            'error_type': 'validation_error'
        }), 400
    except Exception as e:
        logger.error(f"Unexpected error in analyze_repository: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'An unexpected error occurred during repository analysis',
            'error_type': 'internal_error'
        }), 500

@github_bp.route('/website-preview/<session_id>', methods=['GET'])
def get_website_preview(session_id):
    """
    Get the generated website HTML for preview.
    
    Args:
        session_id: The session ID from the analysis
        
    Returns:
        HTML content of the generated website
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
        website_result = session_data.get('website_result')
        
        if not website_result:
            return jsonify({
                'status': 'error',
                'message': 'Website not found for this session',
                'error_type': 'website_not_found'
            }), 404
        
        # Return HTML content
        return website_result['html'], 200, {'Content-Type': 'text/html'}
        
    except Exception as e:
        logger.error(f"Error retrieving website preview: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve website preview',
            'error_type': 'preview_error'
        }), 500

@github_bp.route('/session/<session_id>', methods=['GET'])
def get_session_data(session_id):
    """
    Get full session data for a given session ID.
    
    Args:
        session_id: The session ID from the analysis
        
    Returns:
        Complete session data including analysis and website
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
            'from_cache': session_data.get('from_cache', False),
            'analysis': session_data['analysis_result'],
            'website': {
                'metadata': session_data['website_result']['metadata'],
                'preview_url': f'/api/website-preview/{session_id}'
            }
        })
        
    except Exception as e:
        logger.error(f"Error retrieving session data: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to retrieve session data',
            'error_type': 'retrieval_error'
        }), 500

@github_bp.route('/cache/stats', methods=['GET'])
def get_cache_stats():
    """Get cache service statistics."""
    try:
        stats = cache_service.get_stats()
        return jsonify({
            'status': 'success',
            'cache_stats': stats
        })
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to get cache statistics',
            'error_type': 'cache_error'
        }), 500

@github_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear expired cache entries."""
    try:
        if hasattr(cache_service, 'clear_expired'):
            cleared_count = cache_service.clear_expired()
            return jsonify({
                'status': 'success',
                'message': f'Cleared {cleared_count} expired cache entries'
            })
        else:
            return jsonify({
                'status': 'success',
                'message': 'Cache clear not supported by current cache implementation'
            })
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Failed to clear cache',
            'error_type': 'cache_error'
        }), 500

@github_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for GitHub analysis service."""
    try:
        # Test GitHub API connectivity
        github_health = "healthy"
        try:
            # Simple test to check if GitHub token is working
            test_repo = github_analyzer.get_repository_info("octocat", "Hello-World")
            if not test_repo:
                github_health = "degraded"
        except Exception:
            github_health = "unhealthy"
        
        # Get cache health
        cache_health = cache_service.get_stats() if hasattr(cache_service, 'get_stats') else {"status": "unknown"}
        
        return jsonify({
            'status': 'healthy',
            'service': 'github-portfolio-generator',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'components': {
                'github_api': github_health,
                'cache_service': cache_health,
                'website_generator': 'healthy'
            },
            'session_cache_size': len(analysis_cache)
        })
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'service': 'github-portfolio-generator',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@github_bp.route('/demo-repository', methods=['POST'])
def demo_repository_analysis():
    """
    Demo endpoint with mock data for demonstration purposes.
    """
    try:
        data = request.get_json() if request.is_json else {}
        demo_url = data.get('url', 'https://github.com/demo/portfolio')
        
        session_id = str(uuid.uuid4())
        
        # Create realistic mock data
        mock_analysis = {
            'repository_info': {
                'name': 'portfolio-website',
                'full_name': 'demo/portfolio-website',
                'description': 'A beautiful, responsive portfolio website built with React and modern web technologies.',
                'url': demo_url,
                'clone_url': 'https://github.com/demo/portfolio-website.git',
                'homepage': 'https://demo-portfolio.vercel.app',
                'created_at': '2023-01-15T10:30:00Z',
                'updated_at': '2025-01-01T12:00:00Z',
                'stars': 342,
                'forks': 67,
                'language': 'JavaScript',
                'size': 2456,
                'open_issues': 3,
                'license': 'MIT',
                'topics': ['portfolio', 'react', 'typescript', 'tailwindcss', 'responsive']
            },
            'tech_stack': {
                'primary_language': 'JavaScript',
                'languages': ['JavaScript', 'TypeScript', 'CSS', 'HTML'],
                'frameworks': ['React', 'Next.js', 'Tailwind CSS'],
                'tools': ['Vite', 'ESLint', 'Prettier'],
                'deployment': ['Vercel', 'GitHub Actions'],
                'databases': [],
                'confidence_score': 0.95
            },
            'readme_analysis': {
                'title': 'Portfolio Website',
                'description': 'A modern, responsive portfolio website showcasing projects and skills.',
                'installation': 'npm install && npm run dev',
                'usage': 'Visit the deployed site or run locally for development.',
                'features': [
                    'Responsive design that works on all devices',
                    'Modern UI with smooth animations',
                    'Dark mode support',
                    'Fast loading and SEO optimized',
                    'Easy to customize and extend'
                ],
                'tech_stack': ['React', 'TypeScript', 'Tailwind CSS', 'Framer Motion'],
                'demo_url': 'https://demo-portfolio.vercel.app',
                'screenshots': []
            },
            'project_analysis': {
                'project_type': 'frontend_application',
                'complexity_level': 'medium',
                'project_category': 'portfolio',
                'development_status': 'active',
                'deployment_ready': True
            },
            'website_generation': {
                'template_recommendation': 'modern_spa',
                'color_scheme': 'tech_dark',
                'layout_style': 'showcase_focused',
                'sections_needed': ['hero', 'about', 'features', 'tech_stack', 'demo', 'links', 'footer']
            },
            'analysis_metadata': {
                'analyzed_at': datetime.now().isoformat(),
                'analyzer_version': '1.0.0',
                'confidence_score': 0.95,
                'data_sources': ['demo_data']
            }
        }
        
        # Generate website
        website_result = website_generator.generate_website(mock_analysis)
        
        # Store in session cache
        analysis_cache[session_id] = {
            'url': demo_url,
            'timestamp': datetime.now().isoformat(),
            'analysis_result': mock_analysis,
            'website_result': website_result,
            'from_cache': False,
            'is_demo': True
        }
        
        return jsonify({
            'session_id': session_id,
            'status': 'success',
            'from_cache': False,
            'is_demo': True,
            'analysis': {
                'repository_info': mock_analysis.get('repository_info', {}),
                'tech_stack': mock_analysis.get('tech_stack', {}),
                'project_analysis': mock_analysis.get('project_analysis', {}),
                'website_generation': mock_analysis.get('website_generation', {}),
                'readme_analysis': mock_analysis.get('readme_analysis', {})
            },
            'website': {
                'preview_url': f'/api/website-preview/{session_id}',
                'template_type': website_result['metadata']['template_type'],
                'color_scheme': website_result['metadata']['color_scheme'],
                'generated_at': website_result['metadata']['generated_at']
            }
        })
        
    except Exception as e:
        logger.error(f"Demo analysis error: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Demo analysis failed: {str(e)}',
            'error_type': 'demo_error'
        }), 500
def test_github_analysis():
    """Test endpoint for GitHub analysis with a known repository."""
    try:
        data = request.get_json() if request.is_json else {}
        test_url = data.get('url', 'https://github.com/octocat/Hello-World')
        
        logger.info(f"Testing GitHub analysis with: {test_url}")
        
        # Quick analysis test
        session_id = str(uuid.uuid4())
        
        try:
            analysis_result = github_analyzer.analyze_repository(test_url)
            website_result = website_generator.generate_website(analysis_result)
            
            return jsonify({
                'status': 'success',
                'test_url': test_url,
                'session_id': session_id,
                'analysis_preview': {
                    'repository_name': analysis_result.get('repository_info', {}).get('name', 'Unknown'),
                    'language': analysis_result.get('repository_info', {}).get('language', 'Unknown'),
                    'tech_stack': analysis_result.get('tech_stack', {}).get('frameworks', []),
                    'template_type': website_result['metadata']['template_type']
                }
            })
            
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Test analysis failed: {str(e)}',
                'error_type': 'test_error'
            }), 500
        
    except Exception as e:
        logger.error(f"Error in test analysis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Test endpoint failed: {str(e)}',
            'error_type': 'test_error'
        }), 500

# Error handlers
@github_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'error_type': 'not_found'
    }), 404

@github_bp.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'error_type': 'internal_error'
    }), 500