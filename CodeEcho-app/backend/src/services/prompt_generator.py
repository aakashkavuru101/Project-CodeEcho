"""
AI-driven prompt generation service for creating comprehensive prompts from website analysis.
"""
import json
import os
from typing import Dict, Any, List
from openai import OpenAI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptGenerator:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE')
        )
        
    def generate_comprehensive_prompt(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive prompt for recreating a similar website/application.
        
        Args:
            analysis_data (dict): Structured analysis data from WebsiteAnalyzer
            
        Returns:
            dict: Comprehensive prompt in both text and JSON formats
        """
        try:
            logger.info("Generating comprehensive prompt from analysis data")
            
            # Generate different sections of the prompt
            design_prompt = self._generate_design_prompt(analysis_data)
            functionality_prompt = self._generate_functionality_prompt(analysis_data)
            technical_prompt = self._generate_technical_prompt(analysis_data)
            content_prompt = self._generate_content_prompt(analysis_data)
            ux_prompt = self._generate_ux_prompt(analysis_data)
            
            # Combine all sections into a comprehensive prompt
            comprehensive_prompt = self._combine_prompt_sections({
                'design': design_prompt,
                'functionality': functionality_prompt,
                'technical': technical_prompt,
                'content': content_prompt,
                'user_experience': ux_prompt
            }, analysis_data)
            
            # Generate both text and JSON formats
            text_prompt = self._format_as_text(comprehensive_prompt, analysis_data)
            json_prompt = self._format_as_json(comprehensive_prompt, analysis_data)
            
            return {
                'text_format': text_prompt,
                'json_format': json_prompt,
                'sections': comprehensive_prompt,
                'metadata': {
                    'source_url': analysis_data.get('website_info', {}).get('url', ''),
                    'analysis_timestamp': analysis_data.get('timestamp'),
                    'website_type': analysis_data.get('website_info', {}).get('website_type', ''),
                    'primary_purpose': analysis_data.get('website_info', {}).get('primary_purpose', '')
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating prompt: {str(e)}")
            raise Exception(f"Failed to generate prompt: {str(e)}")
    
    def _generate_design_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Generate design-focused prompt section."""
        design_analysis = analysis_data.get('design_analysis', {})
        
        system_prompt = """You are an expert UI/UX designer and prompt engineer. Based on the website analysis data provided, generate a detailed design prompt that would help recreate a similar visual design and user interface. Focus on visual elements, layout, color schemes, typography, and design patterns."""
        
        user_prompt = f"""
        Based on this website analysis data, create a comprehensive design prompt:
        
        Design Analysis:
        - Color Palette: {design_analysis.get('color_palette', {})}
        - Typography: {design_analysis.get('typography', {})}
        - Layout: {design_analysis.get('layout', {})}
        - Design Patterns: {design_analysis.get('design_patterns', [])}
        - Visual Hierarchy: {design_analysis.get('visual_hierarchy', {})}
        - Responsive Design: {design_analysis.get('responsive_design', {})}
        - UI Components: {design_analysis.get('ui_components', [])}
        
        Generate a detailed design prompt that covers:
        1. Overall visual style and aesthetic
        2. Color scheme and palette
        3. Typography choices and hierarchy
        4. Layout structure and grid system
        5. UI components and design patterns
        6. Responsive design considerations
        7. Visual hierarchy and information organization
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating design prompt: {str(e)}")
            return self._fallback_design_prompt(design_analysis)
    
    def _generate_functionality_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Generate functionality-focused prompt section."""
        functionality_analysis = analysis_data.get('functionality_analysis', {})
        
        system_prompt = """You are an expert web developer and product manager. Based on the website analysis data provided, generate a detailed functionality prompt that would help recreate similar features and user interactions. Focus on core features, user interactions, navigation, forms, and interactive elements."""
        
        user_prompt = f"""
        Based on this website analysis data, create a comprehensive functionality prompt:
        
        Functionality Analysis:
        - Core Features: {functionality_analysis.get('core_features', [])}
        - User Interactions: {functionality_analysis.get('user_interactions', {})}
        - Navigation Structure: {functionality_analysis.get('navigation_structure', {})}
        - Form Functionality: {functionality_analysis.get('form_functionality', {})}
        - Search Functionality: {functionality_analysis.get('search_functionality', {})}
        - Social Features: {functionality_analysis.get('social_features', [])}
        - E-commerce Features: {functionality_analysis.get('e_commerce_features', [])}
        
        Generate a detailed functionality prompt that covers:
        1. Core features and capabilities
        2. User interaction patterns
        3. Navigation structure and user flows
        4. Form handling and data collection
        5. Search and filtering capabilities
        6. Interactive elements and their behaviors
        7. Integration requirements
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating functionality prompt: {str(e)}")
            return self._fallback_functionality_prompt(functionality_analysis)
    
    def _generate_technical_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Generate technical implementation prompt section."""
        technical_analysis = analysis_data.get('technical_analysis', {})
        
        system_prompt = """You are an expert software architect and full-stack developer. Based on the website analysis data provided, generate a detailed technical prompt that would help recreate similar technical implementation. Focus on technology stack, performance, security, and modern web development practices."""
        
        user_prompt = f"""
        Based on this website analysis data, create a comprehensive technical implementation prompt:
        
        Technical Analysis:
        - Frontend Technologies: {technical_analysis.get('frontend_technologies', [])}
        - Frameworks Detected: {technical_analysis.get('frameworks_detected', {})}
        - Performance Metrics: {technical_analysis.get('performance_metrics', {})}
        - Modern Features: {technical_analysis.get('modern_features', [])}
        - SEO Implementation: {technical_analysis.get('seo_implementation', {})}
        - Security Features: {technical_analysis.get('security_features', {})}
        
        Generate a detailed technical prompt that covers:
        1. Recommended technology stack
        2. Frontend framework and libraries
        3. Performance optimization strategies
        4. SEO implementation requirements
        5. Security considerations
        6. Modern web features and APIs
        7. Deployment and hosting recommendations
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating technical prompt: {str(e)}")
            return self._fallback_technical_prompt(technical_analysis)
    
    def _generate_content_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Generate content strategy prompt section."""
        content_analysis = analysis_data.get('content_strategy', {})
        
        system_prompt = """You are an expert content strategist and copywriter. Based on the website analysis data provided, generate a detailed content prompt that would help recreate similar content structure, organization, and strategy. Focus on content types, information architecture, and content presentation."""
        
        user_prompt = f"""
        Based on this website analysis data, create a comprehensive content strategy prompt:
        
        Content Strategy Analysis:
        - Content Structure: {content_analysis.get('content_structure', {})}
        - Content Types: {content_analysis.get('content_types', [])}
        - Information Architecture: {content_analysis.get('information_architecture', {})}
        - Content Presentation: {content_analysis.get('content_presentation', {})}
        - Multimedia Usage: {content_analysis.get('multimedia_usage', {})}
        
        Generate a detailed content prompt that covers:
        1. Content structure and organization
        2. Types of content to include
        3. Information architecture principles
        4. Content presentation strategies
        5. Multimedia integration approach
        6. Content hierarchy and flow
        7. Copywriting tone and style guidelines
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating content prompt: {str(e)}")
            return self._fallback_content_prompt(content_analysis)
    
    def _generate_ux_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Generate user experience prompt section."""
        ux_analysis = analysis_data.get('user_experience_analysis', {})
        
        system_prompt = """You are an expert UX designer and user researcher. Based on the website analysis data provided, generate a detailed UX prompt that would help recreate similar user experience patterns and flows. Focus on user journeys, accessibility, performance, and engagement strategies."""
        
        user_prompt = f"""
        Based on this website analysis data, create a comprehensive UX design prompt:
        
        UX Analysis:
        - User Journey: {ux_analysis.get('user_journey', {})}
        - Accessibility Features: {ux_analysis.get('accessibility_features', {})}
        - Performance Indicators: {ux_analysis.get('performance_indicators', {})}
        - Mobile Experience: {ux_analysis.get('mobile_experience', {})}
        - Conversion Elements: {ux_analysis.get('conversion_elements', [])}
        - Engagement Features: {ux_analysis.get('engagement_features', [])}
        
        Generate a detailed UX prompt that covers:
        1. User journey mapping and flow design
        2. Accessibility requirements and inclusive design
        3. Performance optimization for user experience
        4. Mobile-first and responsive UX considerations
        5. Conversion optimization strategies
        6. User engagement and retention features
        7. Usability testing and validation approaches
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating UX prompt: {str(e)}")
            return self._fallback_ux_prompt(ux_analysis)
    
    def _combine_prompt_sections(self, sections: Dict[str, str], analysis_data: Dict[str, Any]) -> Dict[str, str]:
        """Combine all prompt sections into a cohesive comprehensive prompt."""
        website_info = analysis_data.get('website_info', {})
        business_model = analysis_data.get('business_model', {})
        
        # Generate an executive summary
        system_prompt = """You are an expert project manager and technical writer. Based on the provided analysis sections, create a cohesive executive summary that ties together all aspects of recreating this website/application. Focus on the overall vision, key requirements, and implementation strategy."""
        
        user_prompt = f"""
        Based on these detailed analysis sections for a {website_info.get('website_type', 'website')} with the primary purpose of {website_info.get('primary_purpose', 'unknown')}, create an executive summary:
        
        Website Information:
        - Type: {website_info.get('website_type', '')}
        - Purpose: {website_info.get('primary_purpose', '')}
        - Target Audience: {website_info.get('target_audience', '')}
        - Industry: {website_info.get('industry_category', '')}
        
        Business Model:
        - Business Type: {business_model.get('business_type', '')}
        - Monetization Strategy: {business_model.get('monetization_strategy', [])}
        - Value Proposition: {business_model.get('value_proposition', '')}
        
        Create a comprehensive executive summary that:
        1. Describes the overall project vision and goals
        2. Outlines key requirements and constraints
        3. Provides a high-level implementation roadmap
        4. Identifies critical success factors
        5. Suggests project timeline and milestones
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            executive_summary = response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            executive_summary = self._fallback_executive_summary(website_info, business_model)
        
        sections['executive_summary'] = executive_summary
        return sections
    
    def _format_as_text(self, sections: Dict[str, str], analysis_data: Dict[str, Any]) -> str:
        """Format the comprehensive prompt as readable text."""
        website_info = analysis_data.get('website_info', {})
        
        text_prompt = f"""# Website Reverse Engineering Prompt

## Project Overview
**Source URL:** {website_info.get('url', 'N/A')}
**Website Type:** {website_info.get('website_type', 'Unknown')}
**Primary Purpose:** {website_info.get('primary_purpose', 'Unknown')}
**Target Audience:** {website_info.get('target_audience', 'Unknown')}
**Industry Category:** {website_info.get('industry_category', 'Unknown')}

## Executive Summary
{sections.get('executive_summary', 'No executive summary available.')}

## Design Requirements
{sections.get('design', 'No design requirements available.')}

## Functionality Requirements
{sections.get('functionality', 'No functionality requirements available.')}

## Technical Implementation
{sections.get('technical', 'No technical requirements available.')}

## Content Strategy
{sections.get('content', 'No content strategy available.')}

## User Experience Guidelines
{sections.get('user_experience', 'No UX guidelines available.')}

## Implementation Notes
- This prompt is generated from automated analysis of the source website
- Adapt and modify requirements based on your specific needs and constraints
- Consider conducting user research to validate assumptions
- Test implementations across different devices and browsers
- Ensure compliance with accessibility standards and legal requirements

---
*Generated by Website Reverse Engineering Tool*
"""
        return text_prompt
    
    def _format_as_json(self, sections: Dict[str, str], analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format the comprehensive prompt as structured JSON."""
        website_info = analysis_data.get('website_info', {})
        business_model = analysis_data.get('business_model', {})
        
        json_prompt = {
            "project_overview": {
                "source_url": website_info.get('url', ''),
                "website_type": website_info.get('website_type', ''),
                "primary_purpose": website_info.get('primary_purpose', ''),
                "target_audience": website_info.get('target_audience', ''),
                "industry_category": website_info.get('industry_category', ''),
                "business_type": business_model.get('business_type', ''),
                "monetization_strategy": business_model.get('monetization_strategy', []),
                "value_proposition": business_model.get('value_proposition', '')
            },
            "requirements": {
                "executive_summary": sections.get('executive_summary', ''),
                "design": {
                    "description": sections.get('design', ''),
                    "color_palette": analysis_data.get('design_analysis', {}).get('color_palette', {}),
                    "typography": analysis_data.get('design_analysis', {}).get('typography', {}),
                    "layout": analysis_data.get('design_analysis', {}).get('layout', {}),
                    "ui_components": analysis_data.get('design_analysis', {}).get('ui_components', [])
                },
                "functionality": {
                    "description": sections.get('functionality', ''),
                    "core_features": analysis_data.get('functionality_analysis', {}).get('core_features', []),
                    "user_interactions": analysis_data.get('functionality_analysis', {}).get('user_interactions', {}),
                    "navigation_structure": analysis_data.get('functionality_analysis', {}).get('navigation_structure', {})
                },
                "technical": {
                    "description": sections.get('technical', ''),
                    "frontend_technologies": analysis_data.get('technical_analysis', {}).get('frontend_technologies', []),
                    "frameworks_detected": analysis_data.get('technical_analysis', {}).get('frameworks_detected', {}),
                    "modern_features": analysis_data.get('technical_analysis', {}).get('modern_features', [])
                },
                "content": {
                    "description": sections.get('content', ''),
                    "content_structure": analysis_data.get('content_strategy', {}).get('content_structure', {}),
                    "content_types": analysis_data.get('content_strategy', {}).get('content_types', []),
                    "multimedia_usage": analysis_data.get('content_strategy', {}).get('multimedia_usage', {})
                },
                "user_experience": {
                    "description": sections.get('user_experience', ''),
                    "user_journey": analysis_data.get('user_experience_analysis', {}).get('user_journey', {}),
                    "accessibility_features": analysis_data.get('user_experience_analysis', {}).get('accessibility_features', {}),
                    "mobile_experience": analysis_data.get('user_experience_analysis', {}).get('mobile_experience', {})
                }
            },
            "implementation_guidelines": {
                "development_approach": "Agile/iterative development recommended",
                "testing_strategy": "Cross-browser and device testing required",
                "accessibility_compliance": "WCAG 2.1 AA standards recommended",
                "performance_targets": "Core Web Vitals optimization",
                "deployment_considerations": "Progressive enhancement and graceful degradation"
            },
            "metadata": {
                "generated_timestamp": analysis_data.get('timestamp'),
                "tool_version": "1.0.0",
                "analysis_confidence": "automated_analysis"
            }
        }
        
        return json_prompt
    
    # Fallback methods for when AI generation fails
    
    def _fallback_design_prompt(self, design_analysis: Dict[str, Any]) -> str:
        """Fallback design prompt when AI generation fails."""
        color_palette = design_analysis.get('color_palette', {})
        typography = design_analysis.get('typography', {})
        layout = design_analysis.get('layout', {})
        
        return f"""Design a modern, responsive website with the following characteristics:

Visual Style:
- Color scheme: {color_palette.get('color_scheme', 'professional')} with {color_palette.get('mood', 'neutral')} mood
- Primary colors: {', '.join(color_palette.get('primary_colors', ['#333333', '#ffffff'])[:3])}
- Typography: {typography.get('font_type', 'sans-serif')} fonts with {typography.get('typography_strategy', 'consistent')} hierarchy

Layout Structure:
- Layout type: {layout.get('layout_type', 'modern')}
- Layout pattern: {layout.get('layout_pattern', 'header_footer_layout')}
- Responsive design: {layout.get('responsive', True)}

UI Components:
- Include standard web components: navigation, buttons, forms, and content sections
- Ensure consistent styling and interaction patterns
- Implement hover states and smooth transitions"""
    
    def _fallback_functionality_prompt(self, functionality_analysis: Dict[str, Any]) -> str:
        """Fallback functionality prompt when AI generation fails."""
        core_features = functionality_analysis.get('core_features', [])
        user_interactions = functionality_analysis.get('user_interactions', {})
        
        return f"""Implement the following core functionality:

Core Features:
{chr(10).join(f'- {feature}' for feature in core_features) if core_features else '- Basic website functionality'}

User Interactions:
- Button interactions: {user_interactions.get('button_count', 0)} interactive buttons
- Navigation links: {user_interactions.get('link_count', 0)} navigation elements
- Form inputs: {user_interactions.get('input_count', 0)} input fields
- Interaction complexity: {user_interactions.get('interaction_complexity', 'medium')}

Navigation:
- Implement clear navigation structure
- Include search functionality if needed
- Ensure intuitive user flows"""
    
    def _fallback_technical_prompt(self, technical_analysis: Dict[str, Any]) -> str:
        """Fallback technical prompt when AI generation fails."""
        frontend_tech = technical_analysis.get('frontend_technologies', [])
        modern_features = technical_analysis.get('modern_features', [])
        
        return f"""Technical Implementation Requirements:

Frontend Technologies:
{chr(10).join(f'- {tech}' for tech in frontend_tech) if frontend_tech else '- HTML5, CSS3, JavaScript'}

Modern Features:
{chr(10).join(f'- {feature}' for feature in modern_features) if modern_features else '- Responsive design, Progressive enhancement'}

Performance:
- Optimize for fast loading times
- Implement responsive design
- Ensure cross-browser compatibility
- Follow web standards and best practices"""
    
    def _fallback_content_prompt(self, content_analysis: Dict[str, Any]) -> str:
        """Fallback content prompt when AI generation fails."""
        content_structure = content_analysis.get('content_structure', {})
        content_types = content_analysis.get('content_types', [])
        
        return f"""Content Strategy Guidelines:

Content Structure:
- Content density: {content_structure.get('content_density', 'medium')}
- Structure type: {content_structure.get('structure_type', 'page')}
- Word count target: {content_structure.get('word_count', 500)} words

Content Types:
{chr(10).join(f'- {content_type}' for content_type in content_types) if content_types else '- Text content, Images'}

Organization:
- Use clear headings and hierarchy
- Implement logical content flow
- Include relevant multimedia elements
- Ensure content supports user goals"""
    
    def _fallback_ux_prompt(self, ux_analysis: Dict[str, Any]) -> str:
        """Fallback UX prompt when AI generation fails."""
        user_journey = ux_analysis.get('user_journey', {})
        mobile_experience = ux_analysis.get('mobile_experience', {})
        
        return f"""User Experience Guidelines:

User Journey:
- Entry points: {', '.join(user_journey.get('entry_points', ['homepage']))}
- Conversion points: {', '.join(user_journey.get('conversion_points', ['contact']))}
- Journey complexity: {user_journey.get('journey_complexity', 'simple')}

Mobile Experience:
- Mobile responsive: {mobile_experience.get('mobile_responsive', True)}
- Mobile optimization: {mobile_experience.get('mobile_optimization', 'basic')}

Accessibility:
- Follow WCAG guidelines
- Ensure keyboard navigation
- Provide alternative text for images
- Use semantic HTML structure"""
    
    def _fallback_executive_summary(self, website_info: Dict[str, Any], business_model: Dict[str, Any]) -> str:
        """Fallback executive summary when AI generation fails."""
        return f"""Project Vision:
Create a {website_info.get('website_type', 'modern')} website that serves the primary purpose of {website_info.get('primary_purpose', 'providing information')} for {website_info.get('target_audience', 'target users')}.

Key Requirements:
- Implement responsive design for all devices
- Ensure fast loading times and good performance
- Follow modern web development best practices
- Include necessary functionality for user goals
- Maintain professional appearance and usability

Implementation Strategy:
- Use modern web technologies and frameworks
- Follow agile development methodology
- Implement progressive enhancement
- Ensure accessibility compliance
- Test across multiple browsers and devices

Success Factors:
- User-centered design approach
- Performance optimization
- SEO-friendly implementation
- Scalable and maintainable code
- Comprehensive testing and validation"""

