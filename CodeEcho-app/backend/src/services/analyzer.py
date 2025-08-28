"""
Website analyzer service for processing scraped data and extracting meaningful insights.
"""
import json
import re
from typing import Dict, List, Any
from collections import Counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebsiteAnalyzer:
    def __init__(self):
        self.analysis_result = {}
    
    def analyze_scraped_data(self, scraped_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze scraped website data to extract structured insights for prompt generation.
        
        Args:
            scraped_data (dict): Raw scraped data from WebsiteScraper
            
        Returns:
            dict: Structured analysis results
        """
        try:
            logger.info(f"Analyzing scraped data for {scraped_data.get('url', 'unknown URL')}")
            
            analysis = {
                'website_info': self._extract_basic_info(scraped_data),
                'design_analysis': self._analyze_design_elements(scraped_data),
                'functionality_analysis': self._analyze_functionality(scraped_data),
                'user_experience_analysis': self._analyze_user_experience(scraped_data),
                'technical_analysis': self._analyze_technical_stack(scraped_data),
                'content_strategy': self._analyze_content_strategy(scraped_data),
                'business_model': self._infer_business_model(scraped_data)
            }
            
            self.analysis_result = analysis
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing scraped data: {str(e)}")
            raise Exception(f"Failed to analyze website data: {str(e)}")
    
    def _extract_basic_info(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract basic website information."""
        return {
            'url': data.get('url', ''),
            'title': data.get('title', ''),
            'website_type': self._classify_website_type(data),
            'primary_purpose': self._determine_primary_purpose(data),
            'target_audience': self._infer_target_audience(data),
            'industry_category': self._classify_industry(data)
        }
    
    def _analyze_design_elements(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visual design elements and patterns."""
        css_info = data.get('css_info', {})
        structure_info = data.get('structure_info', {})
        viewport_info = data.get('viewport_info', {})
        
        # Extract color palette
        colors = css_info.get('colors', [])
        color_palette = self._analyze_color_palette(colors)
        
        # Analyze typography
        fonts = css_info.get('fonts', [])
        typography = self._analyze_typography(fonts, css_info)
        
        # Analyze layout structure
        layout_analysis = self._analyze_layout_structure(structure_info, viewport_info)
        
        # Identify design patterns
        design_patterns = self._identify_design_patterns(data)
        
        return {
            'color_palette': color_palette,
            'typography': typography,
            'layout': layout_analysis,
            'design_patterns': design_patterns,
            'visual_hierarchy': self._analyze_visual_hierarchy(data),
            'responsive_design': self._analyze_responsive_design(viewport_info),
            'ui_components': self._identify_ui_components(data)
        }
    
    def _analyze_functionality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze website functionality and features."""
        interactive_elements = data.get('interactive_elements', {})
        forms_info = data.get('forms_info', [])
        navigation_info = data.get('navigation_info', {})
        
        return {
            'core_features': self._identify_core_features(data),
            'user_interactions': self._analyze_user_interactions(interactive_elements),
            'navigation_structure': self._analyze_navigation_structure(navigation_info),
            'form_functionality': self._analyze_form_functionality(forms_info),
            'search_functionality': self._analyze_search_functionality(data),
            'social_features': self._identify_social_features(data),
            'e_commerce_features': self._identify_ecommerce_features(data)
        }
    
    def _analyze_user_experience(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user experience patterns and flows."""
        return {
            'user_journey': self._map_user_journey(data),
            'accessibility_features': self._analyze_accessibility(data),
            'performance_indicators': self._analyze_performance(data),
            'mobile_experience': self._analyze_mobile_experience(data),
            'conversion_elements': self._identify_conversion_elements(data),
            'engagement_features': self._identify_engagement_features(data)
        }
    
    def _analyze_technical_stack(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical implementation details."""
        tech_info = data.get('technical_info', {})
        
        return {
            'frontend_technologies': self._identify_frontend_tech(tech_info),
            'frameworks_detected': tech_info.get('frameworks', {}),
            'performance_metrics': self._extract_performance_metrics(tech_info),
            'modern_features': self._identify_modern_features(tech_info),
            'seo_implementation': self._analyze_seo_features(data),
            'security_features': self._analyze_security_features(data)
        }
    
    def _analyze_content_strategy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content organization and strategy."""
        content_analysis = data.get('content_analysis', {})
        
        return {
            'content_structure': self._analyze_content_structure(content_analysis),
            'content_types': self._identify_content_types(data),
            'information_architecture': self._analyze_information_architecture(data),
            'content_presentation': self._analyze_content_presentation(data),
            'multimedia_usage': self._analyze_multimedia_usage(data)
        }
    
    def _infer_business_model(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Infer business model and monetization strategy."""
        return {
            'business_type': self._classify_business_type(data),
            'monetization_strategy': self._identify_monetization_strategy(data),
            'value_proposition': self._extract_value_proposition(data),
            'competitive_advantages': self._identify_competitive_advantages(data)
        }
    
    # Helper methods for detailed analysis
    
    def _classify_website_type(self, data: Dict[str, Any]) -> str:
        """Classify the type of website based on content and structure."""
        content = data.get('content_analysis', {})
        forms = data.get('forms_info', [])
        interactive = data.get('interactive_elements', {})
        
        # Check for e-commerce indicators
        if (content.get('has_pricing', False) or 
            any('cart' in str(form).lower() or 'checkout' in str(form).lower() for form in forms)):
            return 'e-commerce'
        
        # Check for blog/content site
        if content.get('paragraph_count', 0) > 10 and content.get('word_count', 0) > 1000:
            return 'blog/content'
        
        # Check for portfolio
        if content.get('has_gallery', False):
            return 'portfolio'
        
        # Check for business/corporate
        if any('contact' in str(form).lower() for form in forms):
            return 'business/corporate'
        
        # Check for landing page
        if content.get('has_hero_section', False) and len(interactive.get('buttons', [])) > 2:
            return 'landing_page'
        
        # Check for application/tool
        if len(forms) > 2 or len(interactive.get('inputs', [])) > 5:
            return 'web_application'
        
        return 'informational'
    
    def _determine_primary_purpose(self, data: Dict[str, Any]) -> str:
        """Determine the primary purpose of the website."""
        website_type = self._classify_website_type(data)
        forms = data.get('forms_info', [])
        
        purpose_map = {
            'e-commerce': 'sell products/services',
            'blog/content': 'share information/content',
            'portfolio': 'showcase work/skills',
            'business/corporate': 'promote business/services',
            'landing_page': 'convert visitors/generate leads',
            'web_application': 'provide tools/functionality',
            'informational': 'provide information'
        }
        
        return purpose_map.get(website_type, 'unknown')
    
    def _analyze_color_palette(self, colors: List[str]) -> Dict[str, Any]:
        """Analyze the color palette used in the website."""
        if not colors:
            return {'primary_colors': [], 'color_scheme': 'unknown', 'mood': 'neutral'}
        
        # Simple color analysis (could be enhanced with color theory)
        unique_colors = list(set(colors))[:10]  # Limit to top 10 unique colors
        
        # Determine color scheme type
        color_scheme = 'monochromatic'
        if len(unique_colors) > 3:
            color_scheme = 'varied'
        elif len(unique_colors) > 1:
            color_scheme = 'complementary'
        
        return {
            'primary_colors': unique_colors,
            'color_scheme': color_scheme,
            'total_colors_used': len(colors),
            'mood': self._infer_color_mood(unique_colors)
        }
    
    def _analyze_typography(self, fonts: List[str], css_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze typography choices and hierarchy."""
        if not fonts:
            return {'primary_font': 'default', 'font_strategy': 'system_default'}
        
        primary_font = css_info.get('primaryFont', fonts[0] if fonts else 'default')
        
        # Classify font types
        serif_indicators = ['serif', 'times', 'georgia', 'garamond']
        sans_serif_indicators = ['sans', 'arial', 'helvetica', 'roboto', 'open sans']
        
        font_type = 'unknown'
        for font in fonts:
            font_lower = font.lower()
            if any(indicator in font_lower for indicator in serif_indicators):
                font_type = 'serif'
                break
            elif any(indicator in font_lower for indicator in sans_serif_indicators):
                font_type = 'sans-serif'
                break
        
        return {
            'primary_font': primary_font,
            'font_type': font_type,
            'font_variety': len(set(fonts)),
            'typography_strategy': 'varied' if len(set(fonts)) > 2 else 'consistent'
        }
    
    def _analyze_layout_structure(self, structure: Dict[str, Any], viewport: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the layout structure and organization."""
        layout_type = structure.get('layoutType', 'traditional')
        
        layout_components = {
            'has_header': structure.get('hasHeader', False),
            'has_footer': structure.get('hasFooter', False),
            'has_navigation': structure.get('hasNavigation', False),
            'has_sidebar': structure.get('hasSidebar', False),
            'main_content_area': structure.get('mainContentArea', False)
        }
        
        # Determine layout pattern
        if layout_components['has_sidebar']:
            layout_pattern = 'sidebar_layout'
        elif layout_components['has_header'] and layout_components['has_footer']:
            layout_pattern = 'header_footer_layout'
        else:
            layout_pattern = 'simple_layout'
        
        return {
            'layout_type': layout_type,
            'layout_pattern': layout_pattern,
            'components': layout_components,
            'responsive': viewport.get('isMobile', False) or viewport.get('isTablet', False)
        }
    
    def _identify_design_patterns(self, data: Dict[str, Any]) -> List[str]:
        """Identify common design patterns used."""
        patterns = []
        content = data.get('content_analysis', {})
        structure = data.get('structure_info', {})
        
        if content.get('has_hero_section', False):
            patterns.append('hero_section')
        if content.get('has_testimonials', False):
            patterns.append('testimonials')
        if content.get('has_pricing', False):
            patterns.append('pricing_table')
        if content.get('has_gallery', False):
            patterns.append('image_gallery')
        if structure.get('hasNavigation', False):
            patterns.append('navigation_menu')
        
        return patterns
    
    def _identify_core_features(self, data: Dict[str, Any]) -> List[str]:
        """Identify the core features of the website."""
        features = []
        forms = data.get('forms_info', [])
        interactive = data.get('interactive_elements', {})
        navigation = data.get('navigation_info', {})
        
        # Form-based features
        for form in forms:
            purpose = form.get('purpose', 'unknown')
            if purpose != 'unknown':
                features.append(f"{purpose}_form")
        
        # Navigation features
        if navigation.get('searchBox', False):
            features.append('search_functionality')
        if navigation.get('pagination', False):
            features.append('pagination')
        
        # Interactive features
        if len(interactive.get('buttons', [])) > 3:
            features.append('interactive_interface')
        if len(interactive.get('links', [])) > 10:
            features.append('rich_navigation')
        
        return features
    
    def _infer_color_mood(self, colors: List[str]) -> str:
        """Infer the mood/feeling from color choices."""
        # Simplified color mood analysis
        color_text = ' '.join(colors).lower()
        
        if any(word in color_text for word in ['blue', 'navy', 'cyan']):
            return 'professional/trustworthy'
        elif any(word in color_text for word in ['red', 'orange', 'yellow']):
            return 'energetic/warm'
        elif any(word in color_text for word in ['green', 'forest', 'lime']):
            return 'natural/growth'
        elif any(word in color_text for word in ['purple', 'violet', 'magenta']):
            return 'creative/luxury'
        elif any(word in color_text for word in ['black', 'gray', 'white']):
            return 'minimal/elegant'
        else:
            return 'neutral'
    
    def _analyze_visual_hierarchy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze visual hierarchy and information organization."""
        structure = data.get('structure_info', {})
        
        headings = structure.get('headings', [])
        heading_hierarchy = Counter(headings)
        
        return {
            'heading_structure': dict(heading_hierarchy),
            'has_clear_hierarchy': len(heading_hierarchy) > 1,
            'sections_count': structure.get('sections', 0),
            'content_organization': 'hierarchical' if len(heading_hierarchy) > 2 else 'flat'
        }
    
    def _analyze_responsive_design(self, viewport: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze responsive design implementation."""
        return {
            'is_responsive': viewport.get('hasMediaQueries', False),
            'mobile_optimized': viewport.get('isMobile', False),
            'tablet_optimized': viewport.get('isTablet', False),
            'viewport_configured': True  # Assuming if we got viewport data
        }
    
    def _identify_ui_components(self, data: Dict[str, Any]) -> List[str]:
        """Identify common UI components used."""
        components = []
        interactive = data.get('interactive_elements', {})
        navigation = data.get('navigation_info', {})
        
        if interactive.get('buttons'):
            components.append('buttons')
        if interactive.get('inputs'):
            components.append('form_inputs')
        if interactive.get('selects'):
            components.append('dropdowns')
        if navigation.get('mainNav'):
            components.append('navigation_menu')
        if navigation.get('breadcrumbs'):
            components.append('breadcrumbs')
        if navigation.get('pagination'):
            components.append('pagination')
        
        return components
    
    def _analyze_user_interactions(self, interactive: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user interaction patterns."""
        return {
            'button_count': len(interactive.get('buttons', [])),
            'link_count': len(interactive.get('links', [])),
            'input_count': len(interactive.get('inputs', [])),
            'interaction_complexity': self._calculate_interaction_complexity(interactive),
            'primary_actions': self._identify_primary_actions(interactive)
        }
    
    def _calculate_interaction_complexity(self, interactive: Dict[str, Any]) -> str:
        """Calculate the complexity of user interactions."""
        total_interactions = (
            len(interactive.get('buttons', [])) +
            len(interactive.get('inputs', [])) +
            len(interactive.get('selects', [])) +
            len(interactive.get('textareas', []))
        )
        
        if total_interactions > 20:
            return 'high'
        elif total_interactions > 10:
            return 'medium'
        elif total_interactions > 3:
            return 'low'
        else:
            return 'minimal'
    
    def _identify_primary_actions(self, interactive: Dict[str, Any]) -> List[str]:
        """Identify primary user actions based on button text and types."""
        actions = []
        buttons = interactive.get('buttons', [])
        
        for button in buttons:
            text = button.get('text', '').lower()
            if any(word in text for word in ['submit', 'send', 'contact']):
                actions.append('contact/submit')
            elif any(word in text for word in ['buy', 'purchase', 'order', 'cart']):
                actions.append('purchase')
            elif any(word in text for word in ['sign up', 'register', 'join']):
                actions.append('registration')
            elif any(word in text for word in ['login', 'sign in']):
                actions.append('authentication')
            elif any(word in text for word in ['download', 'get']):
                actions.append('download')
        
        return list(set(actions))
    
    def _analyze_navigation_structure(self, navigation: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze navigation structure and patterns."""
        main_nav = navigation.get('mainNav', [])
        
        return {
            'navigation_items': len(main_nav),
            'has_breadcrumbs': bool(navigation.get('breadcrumbs')),
            'has_search': navigation.get('searchBox', False),
            'navigation_complexity': 'complex' if len(main_nav) > 7 else 'simple',
            'navigation_pattern': self._determine_navigation_pattern(navigation)
        }
    
    def _determine_navigation_pattern(self, navigation: Dict[str, Any]) -> str:
        """Determine the navigation pattern used."""
        main_nav_count = len(navigation.get('mainNav', []))
        has_breadcrumbs = bool(navigation.get('breadcrumbs'))
        
        if main_nav_count > 10:
            return 'mega_menu'
        elif has_breadcrumbs:
            return 'hierarchical'
        elif main_nav_count > 5:
            return 'horizontal_menu'
        else:
            return 'simple_menu'
    
    def _analyze_form_functionality(self, forms: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze form functionality and purposes."""
        if not forms:
            return {'form_count': 0, 'form_types': [], 'complexity': 'none'}
        
        form_purposes = [form.get('purpose', 'unknown') for form in forms]
        total_fields = sum(len(form.get('fields', [])) for form in forms)
        
        return {
            'form_count': len(forms),
            'form_types': list(set(form_purposes)),
            'total_fields': total_fields,
            'complexity': 'high' if total_fields > 20 else 'medium' if total_fields > 10 else 'low'
        }
    
    def _analyze_search_functionality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze search functionality implementation."""
        navigation = data.get('navigation_info', {})
        
        return {
            'has_search': navigation.get('searchBox', False),
            'search_type': 'basic' if navigation.get('searchBox', False) else 'none'
        }
    
    def _identify_social_features(self, data: Dict[str, Any]) -> List[str]:
        """Identify social media and sharing features."""
        # This would need more sophisticated analysis of the HTML content
        # For now, return basic analysis
        return []
    
    def _identify_ecommerce_features(self, data: Dict[str, Any]) -> List[str]:
        """Identify e-commerce specific features."""
        features = []
        content = data.get('content_analysis', {})
        
        if content.get('has_pricing', False):
            features.append('pricing_display')
        
        # Could be enhanced with more sophisticated detection
        return features
    
    def _map_user_journey(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Map potential user journeys through the site."""
        forms = data.get('forms_info', [])
        navigation = data.get('navigation_info', {})
        
        entry_points = ['homepage']
        if navigation.get('searchBox', False):
            entry_points.append('search')
        
        conversion_points = []
        for form in forms:
            purpose = form.get('purpose', 'unknown')
            if purpose in ['contact', 'registration', 'subscription']:
                conversion_points.append(purpose)
        
        return {
            'entry_points': entry_points,
            'conversion_points': conversion_points,
            'journey_complexity': 'complex' if len(conversion_points) > 2 else 'simple'
        }
    
    def _analyze_accessibility(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze accessibility features (basic analysis)."""
        # This would require more detailed HTML analysis
        return {
            'basic_structure': True,  # Assuming basic HTML structure exists
            'semantic_html': True,   # Would need to check for proper semantic tags
            'accessibility_score': 'unknown'  # Would need specialized tools
        }
    
    def _analyze_performance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze performance indicators."""
        tech_info = data.get('technical_info', {})
        
        return {
            'load_time': tech_info.get('loadTime', 0),
            'has_optimization': tech_info.get('hasServiceWorker', False),
            'performance_score': 'unknown'  # Would need specialized analysis
        }
    
    def _analyze_mobile_experience(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze mobile user experience."""
        viewport = data.get('viewport_info', {})
        
        return {
            'mobile_responsive': viewport.get('isMobile', False),
            'viewport_configured': True,
            'mobile_optimization': 'basic' if viewport.get('hasMediaQueries', False) else 'none'
        }
    
    def _identify_conversion_elements(self, data: Dict[str, Any]) -> List[str]:
        """Identify elements designed for conversion."""
        elements = []
        interactive = data.get('interactive_elements', {})
        
        buttons = interactive.get('buttons', [])
        for button in buttons:
            text = button.get('text', '').lower()
            if any(word in text for word in ['buy', 'purchase', 'sign up', 'subscribe', 'download']):
                elements.append('cta_button')
                break
        
        forms = data.get('forms_info', [])
        if any(form.get('purpose') in ['contact', 'subscription', 'registration'] for form in forms):
            elements.append('lead_form')
        
        return elements
    
    def _identify_engagement_features(self, data: Dict[str, Any]) -> List[str]:
        """Identify features designed to engage users."""
        features = []
        content = data.get('content_analysis', {})
        
        if content.get('has_testimonials', False):
            features.append('testimonials')
        if content.get('has_gallery', False):
            features.append('visual_gallery')
        
        return features
    
    def _identify_frontend_tech(self, tech_info: Dict[str, Any]) -> List[str]:
        """Identify frontend technologies used."""
        technologies = []
        
        if tech_info.get('hasJavaScript', False):
            technologies.append('javascript')
        
        frameworks = tech_info.get('frameworks', {})
        for framework, detected in frameworks.items():
            if detected:
                technologies.append(framework)
        
        return technologies
    
    def _extract_performance_metrics(self, tech_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract performance metrics."""
        return {
            'load_time': tech_info.get('loadTime', 0),
            'has_service_worker': tech_info.get('hasServiceWorker', False)
        }
    
    def _identify_modern_features(self, tech_info: Dict[str, Any]) -> List[str]:
        """Identify modern web features."""
        features = []
        
        if tech_info.get('hasServiceWorker', False):
            features.append('service_worker')
        if tech_info.get('isResponsive', False):
            features.append('responsive_design')
        
        return features
    
    def _analyze_seo_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze SEO implementation (basic)."""
        return {
            'has_title': bool(data.get('title')),
            'title_length': len(data.get('title', '')),
            'seo_score': 'basic'  # Would need more detailed analysis
        }
    
    def _analyze_security_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze security features (basic)."""
        url = data.get('url', '')
        
        return {
            'uses_https': url.startswith('https://'),
            'security_score': 'basic'  # Would need more detailed analysis
        }
    
    def _analyze_content_structure(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content structure and organization."""
        return {
            'word_count': content.get('word_count', 0),
            'paragraph_count': content.get('paragraph_count', 0),
            'content_density': 'high' if content.get('word_count', 0) > 1000 else 'medium' if content.get('word_count', 0) > 500 else 'low',
            'structure_type': 'article' if content.get('paragraph_count', 0) > 5 else 'page'
        }
    
    def _identify_content_types(self, data: Dict[str, Any]) -> List[str]:
        """Identify types of content present."""
        content_types = []
        structure = data.get('structure_info', {})
        
        if structure.get('images', 0) > 0:
            content_types.append('images')
        if structure.get('videos', 0) > 0:
            content_types.append('videos')
        if structure.get('articles', 0) > 0:
            content_types.append('articles')
        
        return content_types
    
    def _analyze_information_architecture(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze information architecture."""
        navigation = data.get('navigation_info', {})
        structure = data.get('structure_info', {})
        
        return {
            'navigation_depth': len(navigation.get('mainNav', [])),
            'content_sections': structure.get('sections', 0),
            'architecture_type': 'hierarchical' if navigation.get('breadcrumbs') else 'flat'
        }
    
    def _analyze_content_presentation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze how content is presented."""
        content = data.get('content_analysis', {})
        
        return {
            'uses_lists': content.get('list_count', 0) > 0,
            'uses_tables': content.get('table_count', 0) > 0,
            'presentation_style': 'structured' if content.get('list_count', 0) > 2 else 'narrative'
        }
    
    def _analyze_multimedia_usage(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze multimedia content usage."""
        structure = data.get('structure_info', {})
        
        return {
            'image_count': structure.get('images', 0),
            'video_count': structure.get('videos', 0),
            'multimedia_strategy': 'rich' if structure.get('images', 0) > 5 else 'minimal'
        }
    
    def _classify_business_type(self, data: Dict[str, Any]) -> str:
        """Classify the business type based on website characteristics."""
        website_type = self._classify_website_type(data)
        
        business_map = {
            'e-commerce': 'retail/e-commerce',
            'blog/content': 'media/publishing',
            'portfolio': 'creative/freelance',
            'business/corporate': 'service/corporate',
            'landing_page': 'marketing/lead_generation',
            'web_application': 'saas/technology',
            'informational': 'informational/educational'
        }
        
        return business_map.get(website_type, 'unknown')
    
    def _identify_monetization_strategy(self, data: Dict[str, Any]) -> List[str]:
        """Identify potential monetization strategies."""
        strategies = []
        content = data.get('content_analysis', {})
        forms = data.get('forms_info', [])
        
        if content.get('has_pricing', False):
            strategies.append('direct_sales')
        
        for form in forms:
            purpose = form.get('purpose', 'unknown')
            if purpose == 'subscription':
                strategies.append('subscription')
            elif purpose == 'contact':
                strategies.append('lead_generation')
        
        return strategies
    
    def _extract_value_proposition(self, data: Dict[str, Any]) -> str:
        """Extract the apparent value proposition."""
        website_type = self._classify_website_type(data)
        
        value_props = {
            'e-commerce': 'Product sales and convenience',
            'blog/content': 'Information and insights',
            'portfolio': 'Showcase skills and expertise',
            'business/corporate': 'Professional services',
            'landing_page': 'Specific product/service offering',
            'web_application': 'Tool/service functionality',
            'informational': 'Knowledge and information'
        }
        
        return value_props.get(website_type, 'Unknown value proposition')
    
    def _identify_competitive_advantages(self, data: Dict[str, Any]) -> List[str]:
        """Identify potential competitive advantages."""
        advantages = []
        
        # This would require more sophisticated analysis
        # For now, return basic advantages based on features
        if data.get('technical_info', {}).get('isResponsive', False):
            advantages.append('mobile_responsive')
        
        if data.get('navigation_info', {}).get('searchBox', False):
            advantages.append('search_functionality')
        
        return advantages


    
    def _infer_target_audience(self, data: Dict[str, Any]) -> str:
        """Infer the target audience based on website characteristics."""
        website_type = self._classify_website_type(data)
        content = data.get('content_analysis', {})
        
        audience_map = {
            'e-commerce': 'consumers/shoppers',
            'blog/content': 'readers/information seekers',
            'portfolio': 'potential clients/employers',
            'business/corporate': 'business clients/partners',
            'landing_page': 'potential customers/leads',
            'web_application': 'end users/professionals',
            'informational': 'general public/researchers'
        }
        
        return audience_map.get(website_type, 'general audience')
    
    def _classify_industry(self, data: Dict[str, Any]) -> str:
        """Classify the industry category based on content and purpose."""
        website_type = self._classify_website_type(data)
        title = data.get('title', '').lower()
        
        # Simple industry classification based on keywords and type
        if any(word in title for word in ['tech', 'software', 'app', 'digital']):
            return 'technology'
        elif any(word in title for word in ['shop', 'store', 'buy', 'sell']):
            return 'retail/e-commerce'
        elif any(word in title for word in ['health', 'medical', 'doctor', 'clinic']):
            return 'healthcare'
        elif any(word in title for word in ['education', 'school', 'university', 'learn']):
            return 'education'
        elif any(word in title for word in ['finance', 'bank', 'investment', 'money']):
            return 'finance'
        elif website_type == 'portfolio':
            return 'creative/professional services'
        elif website_type == 'blog/content':
            return 'media/publishing'
        else:
            return 'general/other'

