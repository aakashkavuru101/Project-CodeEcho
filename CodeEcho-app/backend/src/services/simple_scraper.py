"""
Simple website scraper that works without Playwright for environments where browser installation fails.
"""
import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleWebsiteScraper:
    """
    A simple website scraper that uses requests and BeautifulSoup instead of Playwright.
    This is a fallback for environments where Playwright installation fails.
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def scrape_website(self, url: str) -> dict:
        """
        Scrape a website and extract basic information for prompt generation.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            dict: Website analysis data
        """
        try:
            logger.info(f"Scraping website: {url}")
            
            # Fetch the page
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract basic information
            page_title = soup.title.string.strip() if soup.title else "Unknown Title"
            
            # Analyze page structure
            structure_info = self._analyze_page_structure(soup)
            
            # Extract interactive elements
            interactive_elements = self._extract_interactive_elements(soup)
            
            # Analyze navigation
            navigation_info = self._analyze_navigation(soup, url)
            
            # Extract forms
            forms_info = self._extract_forms(soup)
            
            # Analyze content patterns
            content_analysis = self._analyze_content_patterns(soup)
            
            # Basic CSS/style analysis
            css_info = self._analyze_basic_styles(soup)
            
            # Technical aspects
            tech_info = self._analyze_technical_aspects(soup)
            
            return {
                'url': url,
                'title': page_title,
                'viewport_info': {
                    'width': 1920,
                    'height': 1080,
                    'devicePixelRatio': 1,
                    'hasMediaQueries': bool(soup.find('style') or soup.find('link', rel='stylesheet')),
                    'isMobile': False,
                    'isTablet': False
                },
                'css_info': css_info,
                'structure_info': structure_info,
                'interactive_elements': interactive_elements,
                'navigation_info': navigation_info,
                'forms_info': forms_info,
                'content_analysis': content_analysis,
                'technical_info': tech_info,
                'html_content': str(soup)[:10000],  # Truncate for storage
                'timestamp': 0  # Simple timestamp
            }
            
        except Exception as e:
            logger.error(f"Error scraping website {url}: {str(e)}")
            raise Exception(f"Failed to scrape website: {str(e)}")
    
    def _analyze_page_structure(self, soup: BeautifulSoup) -> dict:
        """Analyze the overall page structure and layout."""
        structure_data = {
            'hasHeader': bool(soup.find(['header', '[class*="header"]', '[id*="header"]'])),
            'hasFooter': bool(soup.find(['footer', '[class*="footer"]', '[id*="footer"]'])),
            'hasNavigation': bool(soup.find(['nav', '[class*="nav"]', '[class*="navigation"]'])),
            'hasSidebar': bool(soup.find(['aside', '[class*="sidebar"]', '[class*="side-nav"]'])),
            'mainContentArea': bool(soup.find(['main', '[class*="main"]', '[class*="content"]', '[id*="content"]'])),
            'layoutType': 'traditional'  # Default since we can't easily detect CSS layout type
        }
        
        # Add semantic analysis
        structure_data.update({
            'headings': [tag.name for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
            'sections': len(soup.find_all('section')),
            'articles': len(soup.find_all('article')),
            'images': len(soup.find_all('img')),
            'videos': len(soup.find_all('video')),
            'iframes': len(soup.find_all('iframe'))
        })
        
        return structure_data
    
    def _extract_interactive_elements(self, soup: BeautifulSoup) -> dict:
        """Extract all interactive elements and their properties."""
        elements = {
            'buttons': [],
            'links': [],
            'inputs': [],
            'selects': [],
            'textareas': []
        }
        
        # Buttons
        for btn in soup.find_all(['button', 'input']):
            if btn.name == 'input' and btn.get('type') not in ['button', 'submit']:
                continue
            elements['buttons'].append({
                'text': btn.get_text(strip=True) or btn.get('value', ''),
                'type': btn.get('type', 'button'),
                'classes': btn.get('class', []),
                'id': btn.get('id', '')
            })
        
        # Links
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            parsed_url = urlparse(href)
            elements['links'].append({
                'text': link.get_text(strip=True),
                'href': href,
                'classes': link.get('class', []),
                'isExternal': bool(parsed_url.netloc)
            })
        
        # Input fields
        for input_field in soup.find_all('input'):
            elements['inputs'].append({
                'type': input_field.get('type', 'text'),
                'placeholder': input_field.get('placeholder', ''),
                'name': input_field.get('name', ''),
                'required': input_field.has_attr('required'),
                'classes': input_field.get('class', [])
            })
        
        # Select dropdowns
        for select in soup.find_all('select'):
            options = [opt.get_text(strip=True) for opt in select.find_all('option')]
            elements['selects'].append({
                'name': select.get('name', ''),
                'options': options,
                'classes': select.get('class', [])
            })
        
        # Textareas
        for textarea in soup.find_all('textarea'):
            elements['textareas'].append({
                'placeholder': textarea.get('placeholder', ''),
                'name': textarea.get('name', ''),
                'classes': textarea.get('class', [])
            })
        
        return elements
    
    def _analyze_navigation(self, soup: BeautifulSoup, base_url: str) -> dict:
        """Analyze navigation structure."""
        navigation = {
            'mainNav': [],
            'breadcrumbs': [],
            'pagination': False,
            'searchBox': False
        }
        
        # Main navigation
        nav_selectors = ['nav a', '[class*="nav"] a', '[class*="navigation"] a', '[class*="menu"] a']
        for selector in nav_selectors:
            for link in soup.select(selector):
                href = link.get('href', '')
                if href:
                    navigation['mainNav'].append({
                        'text': link.get_text(strip=True),
                        'href': urljoin(base_url, href)
                    })
        
        # Breadcrumbs
        breadcrumb_selectors = ['[class*="breadcrumb"] a', '[aria-label*="breadcrumb"] a']
        for selector in breadcrumb_selectors:
            for link in soup.select(selector):
                href = link.get('href', '')
                if href:
                    navigation['breadcrumbs'].append({
                        'text': link.get_text(strip=True),
                        'href': urljoin(base_url, href)
                    })
        
        # Pagination
        navigation['pagination'] = bool(soup.find(['[class*="pagination"]', '[class*="pager"]', '[class*="page-numbers"]']))
        
        # Search box
        navigation['searchBox'] = bool(soup.find(['input[type="search"]', 'input[placeholder*="search" i]', '[class*="search-box"]']))
        
        return navigation
    
    def _extract_forms(self, soup: BeautifulSoup) -> list:
        """Extract form structures and their purposes."""
        forms = []
        
        for form in soup.find_all('form'):
            form_data = {
                'action': form.get('action', ''),
                'method': form.get('method', 'GET').upper(),
                'fields': [],
                'purpose': 'unknown'
            }
            
            # Extract form fields
            for field in form.find_all(['input', 'select', 'textarea']):
                field_data = {
                    'type': field.get('type', field.name),
                    'name': field.get('name', ''),
                    'placeholder': field.get('placeholder', ''),
                    'required': field.has_attr('required'),
                    'label': ''
                }
                
                # Try to find associated label
                field_id = field.get('id')
                if field_id:
                    label = soup.find('label', attrs={'for': field_id})
                    if label:
                        field_data['label'] = label.get_text(strip=True)
                
                form_data['fields'].append(field_data)
            
            # Determine form purpose
            form_text = form.get_text().lower()
            if 'login' in form_text or 'sign in' in form_text:
                form_data['purpose'] = 'login'
            elif 'register' in form_text or 'sign up' in form_text:
                form_data['purpose'] = 'registration'
            elif 'contact' in form_text or 'message' in form_text:
                form_data['purpose'] = 'contact'
            elif 'search' in form_text:
                form_data['purpose'] = 'search'
            elif 'subscribe' in form_text or 'newsletter' in form_text:
                form_data['purpose'] = 'subscription'
            
            forms.append(form_data)
        
        return forms
    
    def _analyze_content_patterns(self, soup: BeautifulSoup) -> dict:
        """Analyze content patterns and structure."""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        text_content = soup.get_text()
        
        return {
            'word_count': len(text_content.split()),
            'paragraph_count': len(soup.find_all('p')),
            'list_count': len(soup.find_all(['ul', 'ol'])),
            'table_count': len(soup.find_all('table')),
            'has_hero_section': bool(soup.find(['section', 'div'], class_=re.compile(r'hero|banner|jumbotron', re.I))),
            'has_testimonials': bool(soup.find(['section', 'div'], class_=re.compile(r'testimonial|review', re.I))),
            'has_pricing': bool(soup.find(['section', 'div'], class_=re.compile(r'pricing|price', re.I))),
            'has_gallery': bool(soup.find(['section', 'div'], class_=re.compile(r'gallery|portfolio', re.I))),
            'content_sections': len(soup.find_all('section'))
        }
    
    def _analyze_basic_styles(self, soup: BeautifulSoup) -> dict:
        """Basic style analysis from HTML attributes."""
        return {
            'primaryFont': 'system-ui, sans-serif',  # Default assumption
            'backgroundColor': '#ffffff',
            'textColor': '#000000',
            'colors': ['#000000', '#ffffff'],  # Basic defaults
            'fonts': ['system-ui', 'sans-serif'],
            'layout': {
                'display': 'block',
                'flexDirection': 'column',
                'gridTemplateColumns': 'none'
            }
        }
    
    def _analyze_technical_aspects(self, soup: BeautifulSoup) -> dict:
        """Analyze technical aspects of the website."""
        return {
            'hasJavaScript': bool(soup.find('script')),
            'frameworks': {
                'react': bool(soup.find('[data-reactroot]') or soup.find(string=re.compile(r'React', re.I))),
                'vue': bool(soup.find(string=re.compile(r'Vue', re.I))),
                'angular': bool(soup.find('[ng-app]') or soup.find(string=re.compile(r'Angular', re.I))),
                'jquery': bool(soup.find(string=re.compile(r'jQuery', re.I)))
            },
            'hasServiceWorker': False,  # Can't detect without browser context
            'isResponsive': bool(soup.find('meta', attrs={'name': 'viewport'})),
            'loadTime': 0  # Can't measure without browser
        }

# Synchronous function for compatibility
def scrape_website_simple(url: str) -> dict:
    """Simple synchronous website scraper."""
    scraper = SimpleWebsiteScraper()
    return scraper.scrape_website(url)