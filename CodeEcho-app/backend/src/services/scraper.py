"""
Website scraper service for extracting content and structure from web pages.
"""
import asyncio
import json
import re
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebsiteScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        
    async def __aenter__(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=True)
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
    
    async def scrape_website(self, url: str) -> dict:
        """
        Scrape a website and extract comprehensive information for prompt generation.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            dict: Comprehensive website analysis data
        """
        try:
            page = await self.context.new_page()
            
            # Navigate to the page
            logger.info(f"Navigating to {url}")
            response = await page.goto(url, wait_until='networkidle', timeout=30000)
            
            if not response or response.status >= 400:
                raise Exception(f"Failed to load page: HTTP {response.status if response else 'No response'}")
            
            # Wait for page to be fully loaded
            await page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(2)  # Additional wait for dynamic content
            
            # Get page content
            html_content = await page.content()
            page_title = await page.title()
            
            # Get viewport dimensions and responsive behavior
            viewport_info = await self._analyze_viewport(page)
            
            # Extract CSS styles
            css_info = await self._extract_css_info(page)
            
            # Analyze page structure
            structure_info = await self._analyze_page_structure(page, html_content)
            
            # Extract interactive elements
            interactive_elements = await self._extract_interactive_elements(page)
            
            # Analyze navigation and user flows
            navigation_info = await self._analyze_navigation(page, url)
            
            # Extract forms and their structure
            forms_info = await self._extract_forms(page)
            
            # Analyze content patterns
            content_analysis = await self._analyze_content_patterns(html_content)
            
            # Get performance and technical info
            tech_info = await self._analyze_technical_aspects(page)
            
            await page.close()
            
            return {
                'url': url,
                'title': page_title,
                'viewport_info': viewport_info,
                'css_info': css_info,
                'structure_info': structure_info,
                'interactive_elements': interactive_elements,
                'navigation_info': navigation_info,
                'forms_info': forms_info,
                'content_analysis': content_analysis,
                'technical_info': tech_info,
                'html_content': html_content[:10000],  # Truncate for storage
                'timestamp': asyncio.get_event_loop().time()
            }
            
        except Exception as e:
            logger.error(f"Error scraping website {url}: {str(e)}")
            raise Exception(f"Failed to scrape website: {str(e)}")
    
    async def _analyze_viewport(self, page) -> dict:
        """Analyze viewport and responsive design."""
        viewport_data = await page.evaluate("""
            () => {
                return {
                    width: window.innerWidth,
                    height: window.innerHeight,
                    devicePixelRatio: window.devicePixelRatio,
                    hasMediaQueries: !!document.querySelector('style, link[rel="stylesheet"]'),
                    isMobile: window.innerWidth <= 768,
                    isTablet: window.innerWidth > 768 && window.innerWidth <= 1024
                };
            }
        """)
        return viewport_data
    
    async def _extract_css_info(self, page) -> dict:
        """Extract CSS information including colors, fonts, and layout."""
        css_data = await page.evaluate("""
            () => {
                const styles = window.getComputedStyle(document.body);
                const colors = new Set();
                const fonts = new Set();
                
                // Extract colors from all elements
                document.querySelectorAll('*').forEach(el => {
                    const style = window.getComputedStyle(el);
                    if (style.color && style.color !== 'rgba(0, 0, 0, 0)') colors.add(style.color);
                    if (style.backgroundColor && style.backgroundColor !== 'rgba(0, 0, 0, 0)') colors.add(style.backgroundColor);
                    if (style.borderColor && style.borderColor !== 'rgba(0, 0, 0, 0)') colors.add(style.borderColor);
                    if (style.fontFamily) fonts.add(style.fontFamily);
                });
                
                return {
                    primaryFont: styles.fontFamily,
                    backgroundColor: styles.backgroundColor,
                    textColor: styles.color,
                    colors: Array.from(colors).slice(0, 20),
                    fonts: Array.from(fonts).slice(0, 10),
                    layout: {
                        display: styles.display,
                        flexDirection: styles.flexDirection,
                        gridTemplateColumns: styles.gridTemplateColumns
                    }
                };
            }
        """)
        return css_data
    
    async def _analyze_page_structure(self, page, html_content: str) -> dict:
        """Analyze the overall page structure and layout."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        structure_data = await page.evaluate("""
            () => {
                const structure = {
                    hasHeader: !!document.querySelector('header, .header, #header'),
                    hasFooter: !!document.querySelector('footer, .footer, #footer'),
                    hasNavigation: !!document.querySelector('nav, .nav, .navigation'),
                    hasSidebar: !!document.querySelector('.sidebar, .side-nav, aside'),
                    mainContentArea: !!document.querySelector('main, .main, .content, #content'),
                    layoutType: 'unknown'
                };
                
                // Determine layout type
                const body = document.body;
                const bodyStyle = window.getComputedStyle(body);
                if (bodyStyle.display === 'grid') {
                    structure.layoutType = 'grid';
                } else if (bodyStyle.display === 'flex') {
                    structure.layoutType = 'flexbox';
                } else {
                    structure.layoutType = 'traditional';
                }
                
                return structure;
            }
        """)
        
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
    
    async def _extract_interactive_elements(self, page) -> dict:
        """Extract all interactive elements and their properties."""
        interactive_data = await page.evaluate("""
            () => {
                const elements = {
                    buttons: [],
                    links: [],
                    inputs: [],
                    selects: [],
                    textareas: []
                };
                
                // Buttons
                document.querySelectorAll('button, input[type="button"], input[type="submit"]').forEach(btn => {
                    elements.buttons.push({
                        text: btn.textContent?.trim() || btn.value || '',
                        type: btn.type || 'button',
                        classes: btn.className,
                        id: btn.id
                    });
                });
                
                // Links
                document.querySelectorAll('a[href]').forEach(link => {
                    elements.links.push({
                        text: link.textContent?.trim() || '',
                        href: link.href,
                        classes: link.className,
                        isExternal: link.hostname !== window.location.hostname
                    });
                });
                
                // Input fields
                document.querySelectorAll('input').forEach(input => {
                    elements.inputs.push({
                        type: input.type,
                        placeholder: input.placeholder || '',
                        name: input.name || '',
                        required: input.required,
                        classes: input.className
                    });
                });
                
                // Select dropdowns
                document.querySelectorAll('select').forEach(select => {
                    elements.selects.push({
                        name: select.name || '',
                        options: Array.from(select.options).map(opt => opt.text),
                        classes: select.className
                    });
                });
                
                // Textareas
                document.querySelectorAll('textarea').forEach(textarea => {
                    elements.textareas.push({
                        placeholder: textarea.placeholder || '',
                        name: textarea.name || '',
                        classes: textarea.className
                    });
                });
                
                return elements;
            }
        """)
        return interactive_data
    
    async def _analyze_navigation(self, page, base_url: str) -> dict:
        """Analyze navigation structure and user flows."""
        nav_data = await page.evaluate("""
            () => {
                const navigation = {
                    mainNav: [],
                    breadcrumbs: [],
                    pagination: false,
                    searchBox: false
                };
                
                // Main navigation
                const navElements = document.querySelectorAll('nav a, .nav a, .navigation a, .menu a');
                navElements.forEach(link => {
                    navigation.mainNav.push({
                        text: link.textContent?.trim() || '',
                        href: link.href
                    });
                });
                
                // Breadcrumbs
                const breadcrumbElements = document.querySelectorAll('.breadcrumb a, .breadcrumbs a, [aria-label*="breadcrumb"] a');
                breadcrumbElements.forEach(link => {
                    navigation.breadcrumbs.push({
                        text: link.textContent?.trim() || '',
                        href: link.href
                    });
                });
                
                // Pagination
                navigation.pagination = !!document.querySelector('.pagination, .pager, .page-numbers');
                
                // Search box
                navigation.searchBox = !!document.querySelector('input[type="search"], input[placeholder*="search" i], .search-box');
                
                return navigation;
            }
        """)
        return nav_data
    
    async def _extract_forms(self, page) -> dict:
        """Extract form structures and their purposes."""
        forms_data = await page.evaluate("""
            () => {
                const forms = [];
                
                document.querySelectorAll('form').forEach(form => {
                    const formData = {
                        action: form.action || '',
                        method: form.method || 'GET',
                        fields: [],
                        purpose: 'unknown'
                    };
                    
                    // Extract form fields
                    form.querySelectorAll('input, select, textarea').forEach(field => {
                        formData.fields.push({
                            type: field.type || field.tagName.toLowerCase(),
                            name: field.name || '',
                            placeholder: field.placeholder || '',
                            required: field.required || false,
                            label: field.labels?.[0]?.textContent?.trim() || ''
                        });
                    });
                    
                    // Determine form purpose
                    const formText = form.textContent?.toLowerCase() || '';
                    if (formText.includes('login') || formText.includes('sign in')) {
                        formData.purpose = 'login';
                    } else if (formText.includes('register') || formText.includes('sign up')) {
                        formData.purpose = 'registration';
                    } else if (formText.includes('contact') || formText.includes('message')) {
                        formData.purpose = 'contact';
                    } else if (formText.includes('search')) {
                        formData.purpose = 'search';
                    } else if (formText.includes('subscribe') || formText.includes('newsletter')) {
                        formData.purpose = 'subscription';
                    }
                    
                    forms.push(formData);
                });
                
                return forms;
            }
        """)
        return forms_data
    
    async def _analyze_content_patterns(self, html_content: str) -> dict:
        """Analyze content patterns and structure."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
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
    
    async def _analyze_technical_aspects(self, page) -> dict:
        """Analyze technical aspects of the website."""
        tech_data = await page.evaluate("""
            () => {
                return {
                    hasJavaScript: !!document.querySelector('script'),
                    frameworks: {
                        react: !!window.React || !!document.querySelector('[data-reactroot]'),
                        vue: !!window.Vue,
                        angular: !!window.angular || !!document.querySelector('[ng-app]'),
                        jquery: !!window.jQuery || !!window.$
                    },
                    hasServiceWorker: 'serviceWorker' in navigator,
                    isResponsive: !!document.querySelector('meta[name="viewport"]'),
                    loadTime: performance.timing.loadEventEnd - performance.timing.navigationStart
                };
            }
        """)
        return tech_data

# Synchronous wrapper for easier use
def scrape_website_sync(url: str) -> dict:
    """Synchronous wrapper for the async scrape_website method."""
    async def _scrape():
        async with WebsiteScraper() as scraper:
            return await scraper.scrape_website(url)
    
    return asyncio.run(_scrape())

