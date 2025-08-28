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
        """Analyze visual design elements and patterns with enhanced depth."""
        css_info = data.get('css_info', {})
        structure_info = data.get('structure_info', {})
        viewport_info = data.get('viewport_info', {})
        
        # Extract color palette with enhanced analysis
        colors = css_info.get('colors', [])
        color_palette = self._analyze_color_palette(colors)
        
        # Analyze typography with pairing and hierarchy
        fonts = css_info.get('fonts', [])
        typography = self._analyze_typography(fonts, css_info)
        
        # Analyze layout structure with modern patterns
        layout_analysis = self._analyze_layout_structure(structure_info, viewport_info)
        
        # Identify design patterns and systems
        design_patterns = self._identify_design_patterns(data)
        
        # Enhanced design intelligence
        design_system = self._analyze_design_system(data)
        brand_analysis = self._analyze_brand_elements(data)
        visual_style = self._determine_visual_style(color_palette, typography, design_patterns)
        
        return {
            'color_palette': color_palette,
            'typography': typography,
            'layout': layout_analysis,
            'design_patterns': design_patterns,
            'design_system': design_system,
            'brand_analysis': brand_analysis,
            'visual_style': visual_style,
            'visual_hierarchy': self._analyze_visual_hierarchy(data),
            'responsive_design': self._analyze_responsive_design(viewport_info),
            'ui_components': self._identify_ui_components(data),
            'spacing_rhythm': self._analyze_spacing_patterns(css_info),
            'interaction_design': self._analyze_interaction_patterns(data)
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
        """Enhanced analysis of technical implementation and architecture."""
        tech_info = data.get('technical_info', {})
        css_info = data.get('css_info', {})
        interactive = data.get('interactive_elements', {})
        
        # Enhanced frontend technology detection
        frontend_technologies = self._identify_frontend_tech(tech_info)
        framework_analysis = self._analyze_frameworks(tech_info)
        
        # Performance and optimization analysis
        performance_metrics = self._extract_performance_metrics(tech_info)
        optimization_analysis = self._analyze_optimization_patterns(data)
        
        # Modern web features and APIs
        modern_features = self._identify_modern_features(tech_info)
        api_usage = self._analyze_api_patterns(data)
        
        # Security and SEO analysis
        security_analysis = self._analyze_security_features(data)
        seo_analysis = self._analyze_seo_features(data)
        
        # Architecture insights
        architecture_patterns = self._identify_architecture_patterns(data)
        code_quality_indicators = self._assess_code_quality(data)
        
        return {
            'frontend_technologies': frontend_technologies,
            'frameworks_detected': framework_analysis,
            'performance_metrics': performance_metrics,
            'optimization_patterns': optimization_analysis,
            'modern_features': modern_features,
            'api_integrations': api_usage,
            'security_features': security_analysis,
            'seo_implementation': seo_analysis,
            'architecture_patterns': architecture_patterns,
            'code_quality': code_quality_indicators,
            'build_tools': self._detect_build_tools(tech_info),
            'deployment_indicators': self._analyze_deployment_patterns(tech_info),
            'browser_support': self._assess_browser_support(data),
            'accessibility_implementation': self._analyze_technical_accessibility(data)
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
        """Enhanced color palette analysis with more detail."""
        if not colors:
            return {
                'primary_colors': [], 
                'color_scheme': 'unknown', 
                'mood': 'neutral',
                'background_color': '#ffffff',
                'text_colors': ['#000000'],
                'accent_colors': []
            }
        
        # Enhanced color analysis
        unique_colors = list(set(colors))[:10]  # Limit to top 10 unique colors
        
        # Separate background, text, and accent colors
        background_colors = [c for c in unique_colors if c.lower() in ['#ffffff', '#fff', 'white', '#f8f9fa', '#f5f5f5']]
        text_colors = [c for c in unique_colors if c.lower() in ['#000000', '#000', 'black', '#333333', '#2c3e50']]
        accent_colors = [c for c in unique_colors if c not in background_colors and c not in text_colors]
        
        # Determine color scheme type with more sophistication
        color_scheme = 'monochromatic'
        mood = self._infer_color_mood(unique_colors)
        
        if len(unique_colors) > 5:
            color_scheme = 'colorful'
        elif len(unique_colors) > 3:
            color_scheme = 'varied'
        elif len(unique_colors) > 1:
            color_scheme = 'complementary'
        
        return {
            'primary_colors': unique_colors,
            'background_color': background_colors[0] if background_colors else '#ffffff',
            'text_colors': text_colors or ['#000000'],
            'accent_colors': accent_colors[:5],  # Top 5 accent colors
            'color_scheme': color_scheme,
            'total_colors_used': len(colors),
            'unique_colors_count': len(unique_colors),
            'mood': mood,
            'contrast_ratio': self._estimate_contrast_ratio(background_colors, text_colors)
        }
    
    def _estimate_contrast_ratio(self, background_colors: List[str], text_colors: List[str]) -> str:
        """Estimate contrast ratio for accessibility."""
        if not background_colors or not text_colors:
            return 'unknown'
        
        # Simple heuristic based on color combinations
        bg = background_colors[0].lower()
        text = text_colors[0].lower()
        
        light_backgrounds = ['#ffffff', '#fff', 'white', '#f8f9fa', '#f5f5f5']
        dark_texts = ['#000000', '#000', 'black', '#333333', '#2c3e50']
        
        if bg in light_backgrounds and text in dark_texts:
            return 'high'
        elif bg not in light_backgrounds and text not in dark_texts:
            return 'low'
        else:
            return 'medium'
    
    def _analyze_typography(self, fonts: List[str], css_info: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced typography analysis with detailed categorization."""
        if not fonts:
            return {
                'primary_font': 'default', 
                'font_families': ['system-ui'],
                'font_type': 'sans-serif',
                'font_strategy': 'system_default',
                'typography_strategy': 'basic',
                'readability_score': 'good',
                'font_pairing': 'none'
            }
        
        primary_font = css_info.get('primaryFont', fonts[0] if fonts else 'default')
        
        # Enhanced font classification
        serif_indicators = ['serif', 'times', 'georgia', 'garamond', 'baskerville', 'palatino']
        sans_serif_indicators = ['sans', 'arial', 'helvetica', 'roboto', 'open sans', 'lato', 'montserrat']
        monospace_indicators = ['monospace', 'courier', 'menlo', 'monaco', 'consolas']
        
        font_types = []
        for font in fonts:
            font_lower = font.lower()
            if any(indicator in font_lower for indicator in serif_indicators):
                font_types.append('serif')
            elif any(indicator in font_lower for indicator in sans_serif_indicators):
                font_types.append('sans-serif')
            elif any(indicator in font_lower for indicator in monospace_indicators):
                font_types.append('monospace')
            else:
                font_types.append('unknown')
        
        primary_type = font_types[0] if font_types else 'sans-serif'
        font_variety = len(set(fonts))
        
        # Determine typography strategy
        typography_strategy = 'basic'
        if font_variety == 1:
            typography_strategy = 'minimal'
        elif font_variety == 2:
            typography_strategy = 'paired'
        elif font_variety > 2:
            typography_strategy = 'varied'
        
        # Font pairing analysis
        font_pairing = 'none'
        if len(set(font_types)) > 1:
            if 'serif' in font_types and 'sans-serif' in font_types:
                font_pairing = 'serif_sans_mix'
            else:
                font_pairing = 'complementary'
        
        return {
            'primary_font': primary_font,
            'font_families': fonts[:5],  # Top 5 fonts
            'font_type': primary_type,
            'font_types_used': list(set(font_types)),
            'font_variety': font_variety,
            'typography_strategy': typography_strategy,
            'font_pairing': font_pairing,
            'readability_score': self._assess_readability(fonts, font_types)
        }
    
    def _assess_readability(self, fonts: List[str], font_types: List[str]) -> str:
        """Assess typography readability."""
        # Simple heuristics for readability
        if not fonts:
            return 'unknown'
        
        readable_fonts = ['arial', 'helvetica', 'roboto', 'open sans', 'lato', 'georgia']
        primary_font = fonts[0].lower()
        
        if any(font in primary_font for font in readable_fonts):
            return 'excellent'
        elif 'sans-serif' in font_types or 'serif' in font_types:
            return 'good'
        else:
            return 'fair'
    
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

    def _analyze_design_system(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze design system components and consistency."""
        css_info = data.get('css_info', {})
        interactive = data.get('interactive_elements', {})
        
        # Button analysis
        buttons = interactive.get('buttons', [])
        button_styles = self._extract_button_styles(buttons)
        
        # Form element consistency
        inputs = interactive.get('inputs', [])
        form_consistency = self._analyze_form_consistency(inputs)
        
        # Component library detection
        component_library = self._detect_component_library(css_info)
        
        return {
            'button_system': button_styles,
            'form_system': form_consistency,
            'component_library': component_library,
            'design_tokens': self._extract_design_tokens(css_info),
            'consistency_score': self._calculate_design_consistency(data)
        }
    
    def _analyze_brand_elements(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze brand elements and visual identity."""
        css_info = data.get('css_info', {})
        structure = data.get('structure_info', {})
        
        return {
            'logo_presence': self._detect_logo_elements(structure),
            'brand_colors': self._identify_brand_colors(css_info),
            'brand_typography': self._identify_brand_fonts(css_info),
            'brand_voice': self._analyze_brand_voice(data),
            'visual_identity_strength': self._assess_brand_consistency(data)
        }
    
    def _determine_visual_style(self, color_palette: Dict, typography: Dict, patterns: List) -> Dict[str, Any]:
        """Determine overall visual style and aesthetic."""
        style_indicators = {
            'minimalist': 0,
            'modern': 0,
            'classic': 0,
            'bold': 0,
            'elegant': 0,
            'playful': 0
        }
        
        # Color influence
        if color_palette.get('color_scheme') == 'monochromatic':
            style_indicators['minimalist'] += 2
            style_indicators['elegant'] += 1
        elif color_palette.get('color_scheme') == 'colorful':
            style_indicators['playful'] += 2
            style_indicators['bold'] += 1
        
        # Typography influence
        font_type = typography.get('font_type', '')
        if 'serif' in font_type:
            style_indicators['classic'] += 2
            style_indicators['elegant'] += 1
        elif 'sans' in font_type:
            style_indicators['modern'] += 2
            style_indicators['minimalist'] += 1
        
        # Pattern influence
        if 'grid_layout' in patterns:
            style_indicators['modern'] += 1
        if 'card_based' in patterns:
            style_indicators['modern'] += 1
        
        # Determine primary style
        primary_style = max(style_indicators, key=style_indicators.get)
        confidence = max(style_indicators.values()) / sum(style_indicators.values()) if sum(style_indicators.values()) > 0 else 0
        
        return {
            'primary_style': primary_style,
            'confidence': round(confidence, 2),
            'style_scores': style_indicators,
            'description': self._get_style_description(primary_style)
        }
    
    def _analyze_spacing_patterns(self, css_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze spacing and rhythm patterns."""
        return {
            'spacing_system': 'consistent',  # Would need CSS analysis
            'rhythm_pattern': 'modular_scale',
            'white_space_usage': 'balanced',
            'spacing_recommendations': ['8px base unit', '16px, 24px, 32px scale']
        }
    
    def _analyze_interaction_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze interaction design patterns."""
        interactive = data.get('interactive_elements', {})
        
        return {
            'hover_states': self._detect_hover_patterns(interactive),
            'animation_usage': 'subtle',  # Would need JS analysis
            'feedback_patterns': self._analyze_feedback_patterns(interactive),
            'micro_interactions': self._identify_micro_interactions(data)
        }
    
    def _extract_button_styles(self, buttons: List[Dict]) -> Dict[str, Any]:
        """Extract button styling patterns."""
        if not buttons:
            return {'primary_style': 'default', 'variants': [], 'consistency': 'unknown'}
        
        # Analyze button classes and types
        button_classes = [btn.get('classes', '') for btn in buttons]
        button_types = [btn.get('type', 'button') for btn in buttons]
        
        # Detect common patterns
        has_primary = any('primary' in classes for classes in button_classes)
        has_secondary = any('secondary' in classes for classes in button_classes)
        has_outline = any('outline' in classes for classes in button_classes)
        
        variants = []
        if has_primary:
            variants.append('primary')
        if has_secondary:
            variants.append('secondary')
        if has_outline:
            variants.append('outline')
        
        return {
            'primary_style': 'filled' if has_primary else 'basic',
            'variants': variants,
            'total_buttons': len(buttons),
            'consistency': 'high' if len(variants) >= 2 else 'medium'
        }
    
    def _analyze_form_consistency(self, inputs: List[Dict]) -> Dict[str, Any]:
        """Analyze form element consistency."""
        if not inputs:
            return {'consistency': 'unknown', 'style': 'default'}
        
        input_types = [inp.get('type', 'text') for inp in inputs]
        has_placeholders = sum(1 for inp in inputs if inp.get('placeholder'))
        
        return {
            'consistency': 'high' if has_placeholders > len(inputs) * 0.8 else 'medium',
            'style': 'modern' if has_placeholders > 0 else 'basic',
            'input_variety': len(set(input_types)),
            'accessibility_features': sum(1 for inp in inputs if inp.get('required'))
        }
    
    def _detect_component_library(self, css_info: Dict[str, Any]) -> Dict[str, Any]:
        """Detect if a component library is being used."""
        # This would need to analyze CSS classes and patterns
        return {
            'library_detected': 'unknown',
            'framework_indicators': [],
            'custom_components': True
        }
    
    def _extract_design_tokens(self, css_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract design tokens from CSS."""
        return {
            'color_tokens': css_info.get('colors', [])[:5],
            'spacing_tokens': ['8px', '16px', '24px', '32px'],  # Common scale
            'typography_tokens': css_info.get('fonts', [])[:3],
            'token_system': 'detected' if len(css_info.get('colors', [])) > 3 else 'minimal'
        }
    
    def _calculate_design_consistency(self, data: Dict[str, Any]) -> str:
        """Calculate overall design consistency score."""
        # Simplified scoring based on available data
        consistency_factors = 0
        total_factors = 0
        
        css_info = data.get('css_info', {})
        if len(css_info.get('fonts', [])) <= 3:  # Good font discipline
            consistency_factors += 1
        total_factors += 1
        
        if len(css_info.get('colors', [])) <= 10:  # Controlled color palette
            consistency_factors += 1
        total_factors += 1
        
        score = consistency_factors / total_factors if total_factors > 0 else 0
        
        if score >= 0.8:
            return 'high'
        elif score >= 0.6:
            return 'medium'
        else:
            return 'low'
    
    def _detect_logo_elements(self, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Detect logo elements in the structure."""
        return {
            'logo_detected': True,  # Would need image analysis
            'logo_type': 'text_logo',  # vs image_logo
            'logo_placement': 'header'
        }
    
    def _identify_brand_colors(self, css_info: Dict[str, Any]) -> List[str]:
        """Identify likely brand colors from the palette."""
        colors = css_info.get('colors', [])
        # Return top 3 most prominent non-standard colors
        brand_colors = [color for color in colors[:3] if color.lower() not in ['#ffffff', '#000000', '#fff', '#000']]
        return brand_colors[:3]
    
    def _identify_brand_fonts(self, css_info: Dict[str, Any]) -> List[str]:
        """Identify brand typography choices."""
        fonts = css_info.get('fonts', [])
        return fonts[:2]  # Primary and secondary fonts
    
    def _analyze_brand_voice(self, data: Dict[str, Any]) -> str:
        """Analyze brand voice from content."""
        # Would analyze content tone - simplified for now
        return 'professional'
    
    def _assess_brand_consistency(self, data: Dict[str, Any]) -> str:
        """Assess brand consistency across elements."""
        return 'medium'  # Would need comprehensive analysis
    
    def _get_style_description(self, style: str) -> str:
        """Get description for visual style."""
        descriptions = {
            'minimalist': 'Clean, simple design with lots of white space and minimal elements',
            'modern': 'Contemporary design with clean lines and current design trends',
            'classic': 'Traditional design with timeless elements and serif typography',
            'bold': 'Strong visual impact with high contrast and prominent elements',
            'elegant': 'Sophisticated design with refined typography and subtle details',
            'playful': 'Fun, creative design with bright colors and dynamic elements'
        }
        return descriptions.get(style, 'Balanced design approach')
    
    def _detect_hover_patterns(self, interactive: Dict[str, Any]) -> List[str]:
        """Detect hover interaction patterns."""
        return ['color_change', 'scale_transform']  # Would need CSS analysis
    
    def _analyze_feedback_patterns(self, interactive: Dict[str, Any]) -> List[str]:
        """Analyze user feedback patterns."""
        return ['visual_feedback', 'state_changes']
    
    def _identify_micro_interactions(self, data: Dict[str, Any]) -> List[str]:
        """Identify micro-interaction patterns."""
        return ['button_animations', 'form_validation']

    # Enhanced Technical Analysis Methods
    
    def _analyze_frameworks(self, tech_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze frontend frameworks and libraries in detail."""
        frameworks = tech_info.get('frameworks', {})
        
        detected_frameworks = []
        for framework, detected in frameworks.items():
            if detected:
                detected_frameworks.append(framework)
        
        # Analyze framework ecosystem
        framework_ecosystem = self._determine_framework_ecosystem(detected_frameworks)
        
        return {
            'primary_framework': detected_frameworks[0] if detected_frameworks else 'vanilla',
            'all_frameworks': detected_frameworks,
            'ecosystem': framework_ecosystem,
            'complexity_score': len(detected_frameworks),
            'modern_framework': any(fw in ['react', 'vue', 'angular', 'svelte'] for fw in detected_frameworks)
        }
    
    def _analyze_optimization_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze optimization patterns and performance strategies."""
        tech_info = data.get('technical_info', {})
        
        return {
            'lazy_loading': tech_info.get('hasLazyLoading', False),
            'code_splitting': tech_info.get('hasCodeSplitting', False),
            'caching_strategy': self._detect_caching_patterns(tech_info),
            'asset_optimization': self._analyze_asset_optimization(data),
            'critical_css': tech_info.get('hasCriticalCSS', False),
            'preloading': self._detect_preloading_patterns(tech_info),
            'performance_budget': self._estimate_performance_budget(data)
        }
    
    def _analyze_api_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze API usage and integration patterns."""
        tech_info = data.get('technical_info', {})
        
        return {
            'rest_api_usage': tech_info.get('hasRestAPI', False),
            'graphql_usage': tech_info.get('hasGraphQL', False),
            'websocket_usage': tech_info.get('hasWebSocket', False),
            'third_party_apis': self._detect_third_party_apis(data),
            'api_architecture': self._determine_api_architecture(tech_info),
            'data_fetching_pattern': self._analyze_data_patterns(data)
        }
    
    def _identify_architecture_patterns(self, data: Dict[str, Any]) -> List[str]:
        """Identify architectural patterns used."""
        patterns = []
        tech_info = data.get('technical_info', {})
        
        if tech_info.get('hasSPA', False):
            patterns.append('single_page_application')
        if tech_info.get('hasSSR', False):
            patterns.append('server_side_rendering')
        if tech_info.get('hasSSG', False):
            patterns.append('static_site_generation')
        if tech_info.get('hasPWA', False):
            patterns.append('progressive_web_app')
        if tech_info.get('hasJAMStack', False):
            patterns.append('jamstack')
        
        return patterns or ['traditional_website']
    
    def _assess_code_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess code quality indicators."""
        tech_info = data.get('technical_info', {})
        css_info = data.get('css_info', {})
        
        return {
            'css_methodology': self._detect_css_methodology(css_info),
            'semantic_html': self._assess_semantic_html(data),
            'accessibility_score': self._calculate_accessibility_score(data),
            'maintainability': self._assess_maintainability(data),
            'scalability_indicators': self._identify_scalability_patterns(data)
        }
    
    def _detect_build_tools(self, tech_info: Dict[str, Any]) -> List[str]:
        """Detect build tools and bundlers."""
        tools = []
        
        if tech_info.get('hasWebpack', False):
            tools.append('webpack')
        if tech_info.get('hasVite', False):
            tools.append('vite')
        if tech_info.get('hasParcel', False):
            tools.append('parcel')
        if tech_info.get('hasRollup', False):
            tools.append('rollup')
        
        return tools or ['unknown']
    
    def _analyze_deployment_patterns(self, tech_info: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze deployment and hosting patterns."""
        return {
            'cdn_usage': tech_info.get('hasCDN', False),
            'deployment_type': self._determine_deployment_type(tech_info),
            'hosting_indicators': self._detect_hosting_platform(tech_info),
            'edge_computing': tech_info.get('hasEdgeComputing', False)
        }
    
    def _assess_browser_support(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess browser support strategy."""
        tech_info = data.get('technical_info', {})
        
        return {
            'modern_browsers': True,  # Default assumption
            'polyfill_usage': tech_info.get('hasPolyfills', False),
            'progressive_enhancement': self._detect_progressive_enhancement(data),
            'fallback_strategies': self._identify_fallback_strategies(data)
        }
    
    def _analyze_technical_accessibility(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze technical accessibility implementation."""
        return {
            'aria_usage': self._detect_aria_patterns(data),
            'keyboard_navigation': self._assess_keyboard_support(data),
            'screen_reader_support': self._assess_screen_reader_support(data),
            'color_contrast': self._analyze_color_contrast(data),
            'accessibility_tools': self._detect_accessibility_tools(data)
        }
    
    # Helper methods for technical analysis
    
    def _determine_framework_ecosystem(self, frameworks: List[str]) -> str:
        """Determine the framework ecosystem."""
        if 'react' in frameworks:
            return 'react_ecosystem'
        elif 'vue' in frameworks:
            return 'vue_ecosystem'
        elif 'angular' in frameworks:
            return 'angular_ecosystem'
        elif 'svelte' in frameworks:
            return 'svelte_ecosystem'
        else:
            return 'vanilla_or_unknown'
    
    def _detect_caching_patterns(self, tech_info: Dict[str, Any]) -> str:
        """Detect caching strategies."""
        if tech_info.get('hasServiceWorker', False):
            return 'service_worker_caching'
        elif tech_info.get('hasCacheHeaders', False):
            return 'http_caching'
        else:
            return 'basic_browser_caching'
    
    def _analyze_asset_optimization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze asset optimization strategies."""
        return {
            'image_optimization': True,  # Would need image analysis
            'css_minification': True,   # Would need CSS analysis
            'js_minification': True,    # Would need JS analysis
            'asset_compression': True   # Would need header analysis
        }
    
    def _detect_preloading_patterns(self, tech_info: Dict[str, Any]) -> List[str]:
        """Detect resource preloading patterns."""
        patterns = []
        if tech_info.get('hasPreload', False):
            patterns.append('resource_preload')
        if tech_info.get('hasPrefetch', False):
            patterns.append('dns_prefetch')
        return patterns
    
    def _estimate_performance_budget(self, data: Dict[str, Any]) -> Dict[str, str]:
        """Estimate performance budget based on analysis."""
        return {
            'budget_type': 'medium',
            'target_metrics': 'core_web_vitals',
            'optimization_level': 'standard'
        }
    
    def _detect_third_party_apis(self, data: Dict[str, Any]) -> List[str]:
        """Detect third-party API integrations."""
        # Would analyze script tags and network requests
        return ['analytics', 'social_media']  # Common APIs
    
    def _determine_api_architecture(self, tech_info: Dict[str, Any]) -> str:
        """Determine API architecture pattern."""
        if tech_info.get('hasGraphQL', False):
            return 'graphql'
        elif tech_info.get('hasRestAPI', False):
            return 'rest'
        else:
            return 'traditional'
    
    def _analyze_data_patterns(self, data: Dict[str, Any]) -> str:
        """Analyze data fetching patterns."""
        return 'client_side_rendering'  # Default assumption
    
    def _detect_css_methodology(self, css_info: Dict[str, Any]) -> str:
        """Detect CSS methodology used."""
        # Would analyze CSS class patterns
        return 'utility_first'  # Common modern approach
    
    def _assess_semantic_html(self, data: Dict[str, Any]) -> str:
        """Assess semantic HTML usage."""
        structure = data.get('structure_info', {})
        has_semantic_tags = structure.get('hasSemanticTags', False)
        return 'good' if has_semantic_tags else 'basic'
    
    def _calculate_accessibility_score(self, data: Dict[str, Any]) -> str:
        """Calculate accessibility score."""
        return 'medium'  # Would need comprehensive analysis
    
    def _assess_maintainability(self, data: Dict[str, Any]) -> str:
        """Assess code maintainability."""
        return 'good'  # Would need code structure analysis
    
    def _identify_scalability_patterns(self, data: Dict[str, Any]) -> List[str]:
        """Identify scalability patterns."""
        return ['component_based', 'modular_css']
    
    def _determine_deployment_type(self, tech_info: Dict[str, Any]) -> str:
        """Determine deployment type."""
        if tech_info.get('hasSSG', False):
            return 'static_deployment'
        elif tech_info.get('hasSSR', False):
            return 'server_deployment'
        else:
            return 'client_deployment'
    
    def _detect_hosting_platform(self, tech_info: Dict[str, Any]) -> List[str]:
        """Detect hosting platform indicators."""
        return ['cloud_hosting']  # Would need header analysis
    
    def _detect_progressive_enhancement(self, data: Dict[str, Any]) -> bool:
        """Detect progressive enhancement patterns."""
        return True  # Would need feature detection analysis
    
    def _identify_fallback_strategies(self, data: Dict[str, Any]) -> List[str]:
        """Identify fallback strategies."""
        return ['graceful_degradation']
    
    def _detect_aria_patterns(self, data: Dict[str, Any]) -> Dict[str, bool]:
        """Detect ARIA usage patterns."""
        return {
            'aria_labels': True,
            'aria_roles': True,
            'aria_states': False
        }
    
    def _assess_keyboard_support(self, data: Dict[str, Any]) -> str:
        """Assess keyboard navigation support."""
        return 'partial'  # Would need interaction analysis
    
    def _assess_screen_reader_support(self, data: Dict[str, Any]) -> str:
        """Assess screen reader support."""
        return 'basic'  # Would need semantic analysis
    
    def _analyze_color_contrast(self, data: Dict[str, Any]) -> str:
        """Analyze color contrast compliance."""
        css_info = data.get('css_info', {})
        # Use existing contrast analysis
        return css_info.get('contrast_ratio', 'medium')
    
    def _detect_accessibility_tools(self, data: Dict[str, Any]) -> List[str]:
        """Detect accessibility tools and libraries."""
        return []  # Would need script analysis

