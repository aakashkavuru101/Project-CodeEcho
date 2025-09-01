"""
Website Template Generator
Generates beautiful, functional portfolio websites from GitHub repository analysis.
"""
import json
import re
from datetime import datetime
from typing import Dict, List, Any

class WebsiteTemplateGenerator:
    """
    Generates complete HTML websites from repository analysis data.
    """
    
    def __init__(self):
        self.templates = {
            'modern_spa': self._modern_spa_template,
            'professional_service': self._professional_service_template,
            'portfolio_showcase': self._portfolio_showcase_template,
            'api_documentation': self._api_documentation_template,
            'clean_minimal': self._clean_minimal_template
        }
        
        self.color_schemes = {
            'professional_blue': {
                'primary': '#2563eb',
                'secondary': '#1e40af',
                'accent': '#3b82f6',
                'background': '#f8fafc',
                'text': '#1e293b',
                'text_light': '#64748b'
            },
            'vibrant_creative': {
                'primary': '#7c3aed',
                'secondary': '#a855f7',
                'accent': '#c084fc',
                'background': '#faf5ff',
                'text': '#581c87',
                'text_light': '#7c2d12'
            },
            'tech_dark': {
                'primary': '#10b981',
                'secondary': '#059669',
                'accent': '#34d399',
                'background': '#0f172a',
                'text': '#f1f5f9',
                'text_light': '#94a3b8'
            },
            'clean_green': {
                'primary': '#059669',
                'secondary': '#047857',
                'accent': '#10b981',
                'background': '#f0fdf4',
                'text': '#064e3b',
                'text_light': '#059669'
            },
            'modern_minimal': {
                'primary': '#1f2937',
                'secondary': '#374151',
                'accent': '#6b7280',
                'background': '#ffffff',
                'text': '#111827',
                'text_light': '#6b7280'
            }
        }
    
    def generate_website(self, analysis_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate a complete website from repository analysis data.
        
        Args:
            analysis_data: Repository analysis data
            
        Returns:
            Dict containing HTML, CSS, and metadata
        """
        repo_info = analysis_data.get('repository_info', {})
        website_config = analysis_data.get('website_generation', {})
        
        # Get template and styling preferences
        template_type = website_config.get('template_recommendation', 'clean_minimal')
        color_scheme = website_config.get('color_scheme', 'modern_minimal')
        layout_style = website_config.get('layout_style', 'balanced_layout')
        
        # Generate the website
        template_func = self.templates.get(template_type, self._clean_minimal_template)
        html_content = template_func(analysis_data, color_scheme, layout_style)
        
        return {
            'html': html_content,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'template_type': template_type,
                'color_scheme': color_scheme,
                'layout_style': layout_style,
                'repository_name': repo_info.get('name', 'Unknown'),
                'generator_version': '1.0.0'
            }
        }
    
    def _get_color_scheme(self, scheme_name: str) -> Dict[str, str]:
        """Get color scheme by name."""
        return self.color_schemes.get(scheme_name, self.color_schemes['modern_minimal'])
    
    def _format_tech_stack(self, tech_stack: Dict[str, Any]) -> List[str]:
        """Format technology stack for display."""
        formatted = []
        
        # Add primary language
        if tech_stack.get('primary_language'):
            formatted.append(tech_stack['primary_language'])
        
        # Add frameworks
        frameworks = tech_stack.get('frameworks', [])
        formatted.extend(frameworks)
        
        # Add tools
        tools = tech_stack.get('tools', [])
        formatted.extend(tools)
        
        # Remove duplicates and limit to top 8
        return list(dict.fromkeys(formatted))[:8]
    
    def _clean_description(self, description: str) -> str:
        """Clean and format description text."""
        if not description:
            return "A great project built with modern technologies."
        
        # Remove markdown syntax
        description = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', description)
        description = re.sub(r'[*_`#]', '', description)
        
        # Ensure it ends with a period
        if not description.endswith('.'):
            description += '.'
        
        return description.strip()
    
    def _modern_spa_template(self, data: Dict[str, Any], color_scheme: str, layout_style: str) -> str:
        """Generate modern SPA-style template."""
        colors = self._get_color_scheme(color_scheme)
        repo_info = data.get('repository_info', {})
        readme_info = data.get('readme_analysis', {})
        tech_stack = data.get('tech_stack', {})
        
        project_name = repo_info.get('name', 'Project')
        description = self._clean_description(repo_info.get('description', readme_info.get('description', '')))
        technologies = self._format_tech_stack(tech_stack)
        demo_url = repo_info.get('homepage', readme_info.get('demo_url', ''))
        github_url = repo_info.get('url', '')
        features = readme_info.get('features', [])[:6]  # Limit to 6 features
        
        return f"""<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name} - Modern Web Application</title>
    <meta name="description" content="{description}">
    <meta name="author" content="{repo_info.get('full_name', '').split('/')[0] if '/' in repo_info.get('full_name', '') else 'Developer'}">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="{project_name}">
    <meta property="og:description" content="{description}">
    
    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:title" content="{project_name}">
    <meta property="twitter:description" content="{description}">
    
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {{
            --primary: {colors['primary']};
            --secondary: {colors['secondary']};
            --accent: {colors['accent']};
            --background: {colors['background']};
            --text: {colors['text']};
            --text-light: {colors['text_light']};
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: var(--background);
            overflow-x: hidden;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
        }}
        
        /* Navigation */
        nav {{
            position: fixed;
            top: 0;
            width: 100%;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            z-index: 1000;
            padding: 1rem 0;
            transition: all 0.3s ease;
        }}
        
        .nav-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary);
            text-decoration: none;
        }}
        
        .nav-links {{
            display: flex;
            list-style: none;
            gap: 2rem;
        }}
        
        .nav-links a {{
            color: var(--text);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s ease;
        }}
        
        .nav-links a:hover {{
            color: var(--primary);
        }}
        
        /* Hero Section */
        .hero {{
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            background: linear-gradient(135deg, var(--background) 0%, rgba(255,255,255,0.8) 100%);
            position: relative;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><defs><radialGradient id="grad" cx="50%" cy="50%" r="50%"><stop offset="0%" style="stop-color:{colors['primary']};stop-opacity:0.1"/><stop offset="100%" style="stop-color:transparent"/></radialGradient></defs><circle cx="200" cy="200" r="100" fill="url(%23grad)"/><circle cx="800" cy="300" r="150" fill="url(%23grad)"/><circle cx="300" cy="700" r="120" fill="url(%23grad)"/></svg>') no-repeat center;
            background-size: cover;
            opacity: 0.5;
        }}
        
        .hero-content {{
            position: relative;
            z-index: 1;
            max-width: 800px;
        }}
        
        .hero h1 {{
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--primary), var(--accent));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .hero p {{
            font-size: 1.25rem;
            color: var(--text-light);
            margin-bottom: 2rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .cta-buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 1rem 2rem;
            border: none;
            border-radius: 50px;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.3s ease;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .btn-primary {{
            background: var(--primary);
            color: white;
        }}
        
        .btn-primary:hover {{
            background: var(--secondary);
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.15);
        }}
        
        .btn-secondary {{
            background: transparent;
            color: var(--primary);
            border: 2px solid var(--primary);
        }}
        
        .btn-secondary:hover {{
            background: var(--primary);
            color: white;
            transform: translateY(-2px);
        }}
        
        /* Features Section */
        .features {{
            padding: 5rem 0;
            background: var(--background);
        }}
        
        .section-title {{
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 3rem;
            color: var(--text);
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }}
        
        .feature-card {{
            background: white;
            padding: 2rem;
            border-radius: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
            text-align: center;
        }}
        
        .feature-card:hover {{
            transform: translateY(-10px);
        }}
        
        .feature-icon {{
            width: 60px;
            height: 60px;
            background: var(--primary);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            font-size: 1.5rem;
        }}
        
        .feature-card h3 {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text);
        }}
        
        .feature-card p {{
            color: var(--text-light);
        }}
        
        /* Tech Stack Section */
        .tech-stack {{
            padding: 5rem 0;
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            text-align: center;
        }}
        
        .tech-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }}
        
        .tech-item {{
            background: rgba(255,255,255,0.1);
            padding: 1.5rem;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            transition: transform 0.3s ease;
        }}
        
        .tech-item:hover {{
            transform: scale(1.05);
        }}
        
        .tech-item i {{
            font-size: 2rem;
            margin-bottom: 1rem;
            display: block;
        }}
        
        /* Footer */
        footer {{
            background: var(--text);
            color: white;
            padding: 3rem 0;
            text-align: center;
        }}
        
        .footer-content {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .footer-section h3 {{
            margin-bottom: 1rem;
            color: var(--accent);
        }}
        
        .footer-links {{
            list-style: none;
        }}
        
        .footer-links a {{
            color: #ccc;
            text-decoration: none;
            transition: color 0.3s ease;
        }}
        
        .footer-links a:hover {{
            color: var(--accent);
        }}
        
        .social-links {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 2rem;
        }}
        
        .social-links a {{
            width: 40px;
            height: 40px;
            background: var(--primary);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            transition: transform 0.3s ease;
        }}
        
        .social-links a:hover {{
            transform: scale(1.1);
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2.5rem;
            }}
            
            .nav-links {{
                display: none;
            }}
            
            .cta-buttons {{
                flex-direction: column;
                align-items: center;
            }}
            
            .features-grid {{
                grid-template-columns: 1fr;
            }}
            
            .tech-grid {{
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 1rem;
            }}
        }}
        
        /* Animations */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .animate-fade-in {{
            animation: fadeInUp 0.6s ease-out;
        }}
        
        /* Smooth scrolling */
        html {{
            scroll-behavior: smooth;
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="container nav-container">
            <a href="#" class="logo">{project_name}</a>
            <ul class="nav-links">
                <li><a href="#home">Home</a></li>
                <li><a href="#features">Features</a></li>
                <li><a href="#tech">Tech Stack</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <div class="hero-content animate-fade-in">
            <h1>{project_name}</h1>
            <p>{description}</p>
            <div class="cta-buttons">
                {f'<a href="{demo_url}" class="btn btn-primary" target="_blank"><i class="fas fa-external-link-alt"></i> Live Demo</a>' if demo_url else ''}
                {f'<a href="{github_url}" class="btn btn-secondary" target="_blank"><i class="fab fa-github"></i> View Source</a>' if github_url else ''}
            </div>
        </div>
    </section>

    <!-- Features Section -->
    {f'''<section id="features" class="features">
        <div class="container">
            <h2 class="section-title">Key Features</h2>
            <div class="features-grid">
                {self._generate_feature_cards(features)}
            </div>
        </div>
    </section>''' if features else ''}

    <!-- Tech Stack Section -->
    <section id="tech" class="tech-stack">
        <div class="container">
            <h2 class="section-title">Built With</h2>
            <div class="tech-grid">
                {self._generate_tech_items(technologies)}
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer id="contact">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>{project_name}</h3>
                    <p>A modern project showcasing the best practices in web development.</p>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul class="footer-links">
                        {f'<li><a href="{demo_url}" target="_blank">Live Demo</a></li>' if demo_url else ''}
                        {f'<li><a href="{github_url}" target="_blank">Source Code</a></li>' if github_url else ''}
                        <li><a href="#features">Features</a></li>
                        <li><a href="#tech">Technology</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Project Stats</h3>
                    <ul class="footer-links">
                        <li>Stars: {repo_info.get('stars', 0)}</li>
                        <li>Forks: {repo_info.get('forks', 0)}</li>
                        <li>Language: {repo_info.get('language', 'Multiple')}</li>
                        <li>License: {repo_info.get('license', 'Open Source')}</li>
                    </ul>
                </div>
            </div>
            
            <div class="social-links">
                {f'<a href="{github_url}" target="_blank"><i class="fab fa-github"></i></a>' if github_url else ''}
                {f'<a href="{demo_url}" target="_blank"><i class="fas fa-external-link-alt"></i></a>' if demo_url else ''}
            </div>
            
            <p style="margin-top: 2rem; color: #888;">
                © {datetime.now().year} {project_name}. Generated with Portfolio-as-a-Service.
            </p>
        </div>
    </footer>

    <script>
        // Smooth scrolling for navigation links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {{
            anchor.addEventListener('click', function (e) {{
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {{
                    target.scrollIntoView({{
                        behavior: 'smooth',
                        block: 'start'
                    }});
                }}
            }});
        }});

        // Navigation background on scroll
        window.addEventListener('scroll', () => {{
            const nav = document.querySelector('nav');
            if (window.scrollY > 50) {{
                nav.style.background = 'rgba(255, 255, 255, 0.98)';
                nav.style.boxShadow = '0 2px 20px rgba(0,0,0,0.1)';
            }} else {{
                nav.style.background = 'rgba(255, 255, 255, 0.95)';
                nav.style.boxShadow = 'none';
            }}
        }});

        // Animate elements on scroll
        const observerOptions = {{
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        }};

        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.style.animation = 'fadeInUp 0.6s ease-out';
                }}
            }});
        }}, observerOptions);

        // Observe all sections
        document.querySelectorAll('section').forEach(section => {{
            observer.observe(section);
        }});
    </script>
</body>
</html>"""
    
    def _generate_feature_cards(self, features: List[str]) -> str:
        """Generate HTML for feature cards."""
        if not features:
            return ""
        
        icons = ['fas fa-star', 'fas fa-rocket', 'fas fa-shield-alt', 'fas fa-mobile-alt', 'fas fa-bolt', 'fas fa-heart']
        cards = []
        
        for i, feature in enumerate(features):
            icon = icons[i % len(icons)]
            cards.append(f"""
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="{icon}"></i>
                    </div>
                    <h3>{feature.split(':')[0] if ':' in feature else feature}</h3>
                    <p>{feature.split(':', 1)[1].strip() if ':' in feature else 'A powerful feature that enhances the user experience.'}</p>
                </div>
            """)
        
        return ''.join(cards)
    
    def _generate_tech_items(self, technologies: List[str]) -> str:
        """Generate HTML for technology items."""
        tech_icons = {
            'React': 'fab fa-react',
            'Vue.js': 'fab fa-vuejs',
            'Angular': 'fab fa-angular',
            'JavaScript': 'fab fa-js-square',
            'TypeScript': 'fab fa-js-square',
            'Python': 'fab fa-python',
            'Node.js': 'fab fa-node-js',
            'Java': 'fab fa-java',
            'Go': 'fas fa-code',
            'Docker': 'fab fa-docker',
            'AWS': 'fab fa-aws',
            'HTML5': 'fab fa-html5',
            'CSS3': 'fab fa-css3-alt',
            'Git': 'fab fa-git-alt',
            'GitHub': 'fab fa-github',
            'npm': 'fab fa-npm'
        }
        
        items = []
        for tech in technologies:
            icon = tech_icons.get(tech, 'fas fa-code')
            items.append(f"""
                <div class="tech-item">
                    <i class="{icon}"></i>
                    <div>{tech}</div>
                </div>
            """)
        
        return ''.join(items)
    
    def _clean_minimal_template(self, data: Dict[str, Any], color_scheme: str, layout_style: str) -> str:
        """Generate clean minimal template."""
        colors = self._get_color_scheme(color_scheme)
        repo_info = data.get('repository_info', {})
        readme_info = data.get('readme_analysis', {})
        tech_stack = data.get('tech_stack', {})
        
        project_name = repo_info.get('name', 'Project')
        description = self._clean_description(repo_info.get('description', readme_info.get('description', '')))
        technologies = self._format_tech_stack(tech_stack)
        demo_url = repo_info.get('homepage', readme_info.get('demo_url', ''))
        github_url = repo_info.get('url', '')
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{project_name}</title>
    <meta name="description" content="{description}">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: {colors['text']};
            background: {colors['background']};
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }}
        
        header {{
            text-align: center;
            padding: 4rem 0;
            border-bottom: 1px solid #eee;
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            color: {colors['primary']};
            margin-bottom: 1rem;
        }}
        
        .description {{
            font-size: 1.2rem;
            color: {colors['text_light']};
            margin-bottom: 2rem;
        }}
        
        .buttons {{
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .btn-primary {{
            background: {colors['primary']};
            color: white;
        }}
        
        .btn-secondary {{
            background: transparent;
            color: {colors['primary']};
            border: 1px solid {colors['primary']};
        }}
        
        .btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        .section {{
            padding: 3rem 0;
        }}
        
        .section h2 {{
            font-size: 1.5rem;
            margin-bottom: 1.5rem;
            color: {colors['text']};
        }}
        
        .tech-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }}
        
        .tech-tag {{
            background: {colors['primary']};
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 2rem;
        }}
        
        .stat {{
            text-align: center;
            padding: 1rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .stat-number {{
            font-size: 1.5rem;
            font-weight: 700;
            color: {colors['primary']};
        }}
        
        .stat-label {{
            font-size: 0.875rem;
            color: {colors['text_light']};
        }}
        
        footer {{
            text-align: center;
            padding: 2rem 0;
            border-top: 1px solid #eee;
            color: {colors['text_light']};
        }}
        
        @media (max-width: 600px) {{
            .container {{
                padding: 1rem;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            .buttons {{
                flex-direction: column;
                align-items: center;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{project_name}</h1>
            <p class="description">{description}</p>
            <div class="buttons">
                {f'<a href="{demo_url}" class="btn btn-primary" target="_blank"><i class="fas fa-external-link-alt"></i> View Demo</a>' if demo_url else ''}
                {f'<a href="{github_url}" class="btn btn-secondary" target="_blank"><i class="fab fa-github"></i> Source Code</a>' if github_url else ''}
            </div>
        </header>
        
        <main>
            <section class="section">
                <h2><i class="fas fa-code"></i> Technology Stack</h2>
                <div class="tech-list">
                    {self._generate_tech_tags(technologies)}
                </div>
            </section>
            
            <section class="section">
                <h2><i class="fas fa-chart-bar"></i> Project Statistics</h2>
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">{repo_info.get('stars', 0)}</div>
                        <div class="stat-label">Stars</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{repo_info.get('forks', 0)}</div>
                        <div class="stat-label">Forks</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{len(technologies)}</div>
                        <div class="stat-label">Technologies</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{repo_info.get('license', 'MIT')}</div>
                        <div class="stat-label">License</div>
                    </div>
                </div>
            </section>
        </main>
        
        <footer>
            <p>Generated with Portfolio-as-a-Service • © {datetime.now().year}</p>
        </footer>
    </div>
</body>
</html>"""
    
    def _generate_tech_tags(self, technologies: List[str]) -> str:
        """Generate HTML for technology tags."""
        return ''.join([f'<span class="tech-tag">{tech}</span>' for tech in technologies])
    
    def _portfolio_showcase_template(self, data: Dict[str, Any], color_scheme: str, layout_style: str) -> str:
        """Generate portfolio showcase template - simplified version of modern SPA."""
        return self._modern_spa_template(data, color_scheme, layout_style)
    
    def _professional_service_template(self, data: Dict[str, Any], color_scheme: str, layout_style: str) -> str:
        """Generate professional service template - simplified version of modern SPA.""" 
        return self._modern_spa_template(data, color_scheme, layout_style)
    
    def _api_documentation_template(self, data: Dict[str, Any], color_scheme: str, layout_style: str) -> str:
        """Generate API documentation template - simplified version of clean minimal."""
        return self._clean_minimal_template(data, color_scheme, layout_style)