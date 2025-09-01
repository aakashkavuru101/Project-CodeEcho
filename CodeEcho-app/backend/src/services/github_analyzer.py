"""
GitHub Repository Analysis Service
Analyzes GitHub repositories and extracts project information for website generation.
"""
import re
import requests
import base64
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class GitHubAnalyzer:
    """
    Service for analyzing GitHub repositories and extracting project information.
    """
    
    def __init__(self, github_token: str = None):
        """
        Initialize the GitHub analyzer.
        
        Args:
            github_token: GitHub API token for authenticated requests
        """
        self.github_token = github_token
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Portfolio-Generator/1.0'
        }
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
    
    def parse_github_url(self, url: str) -> Dict[str, str]:
        """
        Parse GitHub URL to extract owner and repository name.
        
        Args:
            url: GitHub repository URL
            
        Returns:
            Dict containing owner and repo name
        """
        # Clean up the URL
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
        
        # Parse the URL
        parsed = urlparse(url)
        
        # Extract path parts
        path_parts = [part for part in parsed.path.split('/') if part]
        
        if len(path_parts) < 2:
            raise ValueError("Invalid GitHub URL format. Expected: https://github.com/owner/repo")
        
        owner = path_parts[0]
        repo = path_parts[1]
        
        # Remove .git suffix if present
        if repo.endswith('.git'):
            repo = repo[:-4]
        
        return {
            'owner': owner,
            'repo': repo,
            'full_name': f'{owner}/{repo}'
        }
    
    def get_repository_info(self, owner: str, repo: str) -> Dict[str, Any]:
        """
        Get basic repository information from GitHub API.
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            Repository information
        """
        url = f'https://api.github.com/repos/{owner}/{repo}'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch repository info: {e}")
            raise Exception(f"Failed to fetch repository information: {str(e)}")
    
    def get_repository_contents(self, owner: str, repo: str, path: str = '') -> List[Dict[str, Any]]:
        """
        Get repository contents from GitHub API.
        
        Args:
            owner: Repository owner
            repo: Repository name
            path: Path within the repository
            
        Returns:
            List of repository contents
        """
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{path}'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch repository contents: {e}")
            return []
    
    def get_file_content(self, owner: str, repo: str, file_path: str) -> Optional[str]:
        """
        Get content of a specific file from the repository.
        
        Args:
            owner: Repository owner
            repo: Repository name
            file_path: Path to the file
            
        Returns:
            File content as string or None if not found
        """
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            file_data = response.json()
            if file_data.get('encoding') == 'base64':
                content = base64.b64decode(file_data['content']).decode('utf-8')
                return content
        except Exception as e:
            logger.warning(f"Failed to fetch file {file_path}: {e}")
            return None
    
    def detect_tech_stack(self, contents: List[Dict[str, Any]], repo_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detect technology stack based on repository contents.
        
        Args:
            contents: Repository contents
            repo_info: Repository information
            
        Returns:
            Detected technology stack
        """
        tech_stack = {
            'primary_language': repo_info.get('language', 'Unknown'),
            'languages': [],
            'frameworks': [],
            'tools': [],
            'deployment': [],
            'databases': [],
            'confidence_score': 0.8
        }
        
        # Get languages from GitHub API
        languages_url = repo_info.get('languages_url')
        if languages_url:
            try:
                response = requests.get(languages_url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    languages = response.json()
                    tech_stack['languages'] = list(languages.keys())
            except Exception as e:
                logger.warning(f"Failed to fetch languages: {e}")
        
        # Analyze files to detect frameworks and tools
        file_names = [item['name'].lower() for item in contents if item['type'] == 'file']
        
        # Frontend frameworks
        if 'package.json' in file_names:
            tech_stack['frameworks'].append('Node.js')
            # Could analyze package.json for more specific frameworks
        if any(f.endswith('.vue') for f in file_names):
            tech_stack['frameworks'].append('Vue.js')
        if any(f.endswith('.jsx') or f.endswith('.tsx') for f in file_names):
            tech_stack['frameworks'].append('React')
        if 'angular.json' in file_names:
            tech_stack['frameworks'].append('Angular')
        
        # Backend frameworks
        if 'requirements.txt' in file_names or any(f.endswith('.py') for f in file_names):
            tech_stack['frameworks'].append('Python')
            if 'django' in str(file_names):
                tech_stack['frameworks'].append('Django')
            if 'flask' in str(file_names):
                tech_stack['frameworks'].append('Flask')
        
        if 'pom.xml' in file_names or any(f.endswith('.java') for f in file_names):
            tech_stack['frameworks'].append('Java')
            if 'spring' in str(file_names):
                tech_stack['frameworks'].append('Spring')
        
        if 'go.mod' in file_names or any(f.endswith('.go') for f in file_names):
            tech_stack['frameworks'].append('Go')
        
        # Deployment and tools
        if 'dockerfile' in file_names or 'docker-compose.yml' in file_names:
            tech_stack['deployment'].append('Docker')
        if '.github' in [item['name'] for item in contents if item['type'] == 'dir']:
            tech_stack['tools'].append('GitHub Actions')
        if 'vercel.json' in file_names:
            tech_stack['deployment'].append('Vercel')
        if 'netlify.toml' in file_names:
            tech_stack['deployment'].append('Netlify')
        
        # Databases
        if 'schema.sql' in file_names or 'migration' in str(file_names):
            tech_stack['databases'].append('SQL Database')
        if 'mongodb' in str(file_names) or 'mongo' in str(file_names):
            tech_stack['databases'].append('MongoDB')
        
        return tech_stack
    
    def parse_readme(self, readme_content: str) -> Dict[str, Any]:
        """
        Parse README.md content to extract project information.
        
        Args:
            readme_content: README file content
            
        Returns:
            Parsed README information
        """
        if not readme_content:
            return {}
        
        lines = readme_content.split('\n')
        readme_info = {
            'title': '',
            'description': '',
            'installation': '',
            'usage': '',
            'features': [],
            'tech_stack': [],
            'demo_url': '',
            'screenshots': []
        }
        
        current_section = None
        title_found = False
        
        for line in lines:
            line = line.strip()
            
            # Extract title (first # heading)
            if line.startswith('# ') and not title_found:
                readme_info['title'] = line[2:].strip()
                title_found = True
                continue
            
            # Detect sections
            if line.startswith('## '):
                section = line[3:].lower().strip()
                if 'install' in section:
                    current_section = 'installation'
                elif 'usage' in section or 'getting started' in section:
                    current_section = 'usage'
                elif 'feature' in section:
                    current_section = 'features'
                elif 'tech' in section or 'built with' in section or 'stack' in section:
                    current_section = 'tech_stack'
                else:
                    current_section = None
                continue
            
            # Extract description (first paragraph after title)
            if not readme_info['description'] and line and not line.startswith('#') and not line.startswith('!'):
                readme_info['description'] = line
                continue
            
            # Extract demo URL
            if 'demo' in line.lower() and ('http' in line or 'www' in line):
                urls = re.findall(r'https?://[^\s\)]+', line)
                if urls:
                    readme_info['demo_url'] = urls[0]
            
            # Extract screenshots
            if line.startswith('![') and ('screenshot' in line.lower() or 'demo' in line.lower()):
                urls = re.findall(r'https?://[^\s\)]+', line)
                if urls:
                    readme_info['screenshots'].append(urls[0])
            
            # Add content to current section
            if current_section and line:
                if current_section == 'features' and (line.startswith('- ') or line.startswith('* ')):
                    readme_info['features'].append(line[2:].strip())
                elif current_section == 'tech_stack' and (line.startswith('- ') or line.startswith('* ')):
                    readme_info['tech_stack'].append(line[2:].strip())
                elif current_section in ['installation', 'usage']:
                    readme_info[current_section] += line + '\n'
        
        return readme_info
    
    def analyze_repository(self, github_url: str) -> Dict[str, Any]:
        """
        Perform comprehensive analysis of a GitHub repository.
        
        Args:
            github_url: GitHub repository URL
            
        Returns:
            Complete repository analysis
        """
        try:
            # Parse GitHub URL
            repo_data = self.parse_github_url(github_url)
            owner = repo_data['owner']
            repo = repo_data['repo']
            
            logger.info(f"Starting analysis for repository: {owner}/{repo}")
            
            # Get repository information
            repo_info = self.get_repository_info(owner, repo)
            
            # Get repository contents
            contents = self.get_repository_contents(owner, repo)
            
            # Get README content
            readme_content = self.get_file_content(owner, repo, 'README.md')
            if not readme_content:
                readme_content = self.get_file_content(owner, repo, 'readme.md')
            
            # Detect technology stack
            tech_stack = self.detect_tech_stack(contents, repo_info)
            
            # Parse README
            readme_info = self.parse_readme(readme_content) if readme_content else {}
            
            # Compile analysis result
            analysis_result = {
                'repository_info': {
                    'name': repo_info.get('name', repo),
                    'full_name': repo_info.get('full_name', f'{owner}/{repo}'),
                    'description': repo_info.get('description', readme_info.get('description', '')),
                    'url': github_url,
                    'clone_url': repo_info.get('clone_url', ''),
                    'homepage': repo_info.get('homepage', readme_info.get('demo_url', '')),
                    'created_at': repo_info.get('created_at', ''),
                    'updated_at': repo_info.get('updated_at', ''),
                    'stars': repo_info.get('stargazers_count', 0),
                    'forks': repo_info.get('forks_count', 0),
                    'language': repo_info.get('language', 'Unknown'),
                    'size': repo_info.get('size', 0),
                    'open_issues': repo_info.get('open_issues_count', 0),
                    'license': repo_info.get('license', {}).get('name', 'Unknown') if repo_info.get('license') else 'Unknown',
                    'topics': repo_info.get('topics', [])
                },
                'tech_stack': tech_stack,
                'readme_analysis': readme_info,
                'project_analysis': {
                    'project_type': self._determine_project_type(tech_stack, readme_info, contents),
                    'complexity_level': self._assess_complexity(repo_info, contents, tech_stack),
                    'project_category': self._categorize_project(repo_info, readme_info, tech_stack),
                    'development_status': self._assess_development_status(repo_info),
                    'deployment_ready': self._assess_deployment_readiness(contents),
                },
                'website_generation': {
                    'template_recommendation': self._recommend_template(tech_stack, readme_info),
                    'color_scheme': self._suggest_color_scheme(repo_info, readme_info),
                    'layout_style': self._suggest_layout_style(tech_stack, readme_info),
                    'sections_needed': self._determine_sections_needed(readme_info, repo_info)
                },
                'analysis_metadata': {
                    'analyzed_at': datetime.now().isoformat(),
                    'analyzer_version': '1.0.0',
                    'confidence_score': 0.85,
                    'data_sources': ['github_api', 'readme_analysis', 'file_structure']
                }
            }
            
            logger.info(f"Analysis completed for repository: {owner}/{repo}")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Repository analysis failed: {str(e)}")
            raise Exception(f"Repository analysis failed: {str(e)}")
    
    def _determine_project_type(self, tech_stack: Dict, readme_info: Dict, contents: List) -> str:
        """Determine the type of project based on analysis."""
        frameworks = tech_stack.get('frameworks', [])
        
        if any(fw in frameworks for fw in ['React', 'Vue.js', 'Angular']):
            return 'frontend_application'
        elif any(fw in frameworks for fw in ['Django', 'Flask', 'Spring', 'Express']):
            return 'backend_service'
        elif 'Node.js' in frameworks:
            return 'fullstack_application'
        elif any(f.get('name', '').endswith('.py') for f in contents):
            return 'python_project'
        elif any(f.get('name', '').endswith('.js') for f in contents):
            return 'javascript_project'
        else:
            return 'general_project'
    
    def _assess_complexity(self, repo_info: Dict, contents: List, tech_stack: Dict) -> str:
        """Assess project complexity level."""
        size = repo_info.get('size', 0)
        file_count = len(contents)
        framework_count = len(tech_stack.get('frameworks', []))
        
        if size > 10000 or file_count > 50 or framework_count > 5:
            return 'high'
        elif size > 1000 or file_count > 20 or framework_count > 2:
            return 'medium'
        else:
            return 'low'
    
    def _categorize_project(self, repo_info: Dict, readme_info: Dict, tech_stack: Dict) -> str:
        """Categorize the project type."""
        description = (repo_info.get('description', '') + ' ' + readme_info.get('description', '')).lower()
        topics = repo_info.get('topics', [])
        
        # Check topics and description for categories
        if any(topic in ['portfolio', 'personal-website', 'resume'] for topic in topics):
            return 'portfolio'
        elif any(term in description for term in ['api', 'backend', 'server']):
            return 'api_service'
        elif any(term in description for term in ['web app', 'webapp', 'website']):
            return 'web_application'
        elif any(term in description for term in ['cli', 'command line', 'tool']):
            return 'cli_tool'
        elif any(term in description for term in ['library', 'package', 'module']):
            return 'library'
        elif any(term in description for term in ['game', 'gaming']):
            return 'game'
        else:
            return 'general'
    
    def _assess_development_status(self, repo_info: Dict) -> str:
        """Assess the development status of the project."""
        updated_at = repo_info.get('updated_at', '')
        open_issues = repo_info.get('open_issues_count', 0)
        
        try:
            from datetime import datetime
            last_update = datetime.fromisoformat(updated_at.replace('Z', '+00:00'))
            days_since_update = (datetime.now().replace(tzinfo=last_update.tzinfo) - last_update).days
            
            if days_since_update <= 30:
                return 'active'
            elif days_since_update <= 365:
                return 'maintained'
            else:
                return 'inactive'
        except:
            return 'unknown'
    
    def _assess_deployment_readiness(self, contents: List) -> bool:
        """Assess if the project appears deployment-ready."""
        file_names = [item['name'].lower() for item in contents if item['type'] == 'file']
        
        # Check for deployment configuration files
        deployment_files = [
            'dockerfile', 'docker-compose.yml', 'vercel.json', 'netlify.toml',
            'app.yaml', 'heroku.yml', 'railway.toml', 'render.yaml'
        ]
        
        return any(df in file_names for df in deployment_files)
    
    def _recommend_template(self, tech_stack: Dict, readme_info: Dict) -> str:
        """Recommend a website template based on analysis."""
        frameworks = tech_stack.get('frameworks', [])
        
        if any(fw in frameworks for fw in ['React', 'Vue.js', 'Angular']):
            return 'modern_spa'
        elif any(fw in frameworks for fw in ['Django', 'Flask']):
            return 'professional_service'
        elif 'portfolio' in str(readme_info).lower():
            return 'portfolio_showcase'
        elif 'api' in str(readme_info).lower():
            return 'api_documentation'
        else:
            return 'clean_minimal'
    
    def _suggest_color_scheme(self, repo_info: Dict, readme_info: Dict) -> str:
        """Suggest a color scheme based on project analysis."""
        description = (repo_info.get('description', '') + ' ' + readme_info.get('description', '')).lower()
        
        if any(term in description for term in ['finance', 'bank', 'business']):
            return 'professional_blue'
        elif any(term in description for term in ['creative', 'design', 'art']):
            return 'vibrant_creative'
        elif any(term in description for term in ['tech', 'developer', 'coding']):
            return 'tech_dark'
        elif any(term in description for term in ['health', 'medical', 'care']):
            return 'clean_green'
        else:
            return 'modern_minimal'
    
    def _suggest_layout_style(self, tech_stack: Dict, readme_info: Dict) -> str:
        """Suggest layout style based on project type."""
        if readme_info.get('demo_url') or readme_info.get('screenshots'):
            return 'showcase_focused'
        elif len(readme_info.get('features', [])) > 5:
            return 'feature_rich'
        elif tech_stack.get('primary_language') in ['Python', 'Java', 'Go']:
            return 'documentation_focused'
        else:
            return 'balanced_layout'
    
    def _determine_sections_needed(self, readme_info: Dict, repo_info: Dict) -> List[str]:
        """Determine what sections the generated website should have."""
        sections = ['hero', 'about']
        
        if readme_info.get('features'):
            sections.append('features')
        
        if readme_info.get('demo_url') or readme_info.get('screenshots'):
            sections.append('demo')
        
        if readme_info.get('tech_stack') or repo_info.get('language'):
            sections.append('tech_stack')
        
        if readme_info.get('installation') or readme_info.get('usage'):
            sections.append('getting_started')
        
        sections.extend(['links', 'footer'])
        
        return sections