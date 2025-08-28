"""
AI-driven prompt generation service for creating comprehensive prompts from website analysis.
Uses Ollama for local, secure, and open-source AI model inference.
"""
import json
import os
from typing import Dict, Any, List
import ollama
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PromptGenerator:
    def __init__(self):
        # Ollama model configuration with enhanced multi-modal strategy
        self.models = {
            'primary': 'llama3.1:8b',      # Fast, balanced model for general tasks
            'reasoning': 'qwen2.5:7b',     # Excellent for reasoning and code generation
            'creative': 'mistral:7b',      # Good for creative content generation
            'detailed': 'gemma2:9b',       # Best for detailed, comprehensive responses
            'efficient': 'phi3:medium',    # Microsoft's efficient model for quick tasks
            'code': 'codellama:7b',       # Specialized for code analysis and generation
            'conversational': 'neural-chat:7b',  # Conversational AI for user-focused content
            'instruction': 'vicuna:7b'     # Excellent instruction following for structured tasks
        }
        
        # Enhanced model selection strategy based on task type and complexity
        self.task_models = {
            'design': 'creative',          # Creative tasks benefit from Mistral
            'functionality': 'reasoning',  # Logic and reasoning tasks for Qwen
            'technical': 'code',          # Technical implementation for CodeLlama
            'content': 'conversational',   # Content strategy for Neural-Chat
            'ux': 'detailed',             # UX needs detailed analysis from Gemma
            'analysis': 'reasoning',       # Analysis tasks for Qwen
            'code_generation': 'code',     # Code tasks for CodeLlama
            'user_guidance': 'conversational',  # User-facing content for Neural-Chat
            'structured_output': 'instruction',  # Structured tasks for Vicuna
            'quick_tasks': 'efficient',    # Quick tasks for Phi3
            'default': 'primary'          # Default to balanced Llama
        }
        
        # Multi-modal task routing for complex analyses
        self.complex_task_routing = {
            'comprehensive_analysis': ['reasoning', 'detailed', 'creative'],
            'technical_deep_dive': ['code', 'reasoning', 'detailed'],
            'user_experience_focus': ['conversational', 'creative', 'detailed'],
            'rapid_prototyping': ['efficient', 'code', 'primary']
        }
        
        self.client = ollama.Client()
        self._prompt_cache = {}  # Initialize cache
        self._model_performance_stats = {}  # Track model performance
        self._ensure_models_available()
    
    def _ensure_models_available(self):
        """Check if required models are available, attempt to pull if not."""
        try:
            available_models = [model['name'] for model in self.client.list()['models']]
            logger.info(f"Available Ollama models: {available_models}")
            
            for model_name in self.models.values():
                if model_name not in available_models:
                    logger.info(f"Model {model_name} not found. Attempting to pull...")
                    try:
                        self.client.pull(model_name)
                        logger.info(f"Successfully pulled model: {model_name}")
                    except Exception as e:
                        logger.warning(f"Failed to pull model {model_name}: {str(e)}")
                        
        except Exception as e:
            logger.warning(f"Could not connect to Ollama or check models: {str(e)}")
    
    def _generate_with_fallback(self, prompt: str, task_type: str = 'default', use_multi_modal: bool = False) -> str:
        """Generate content with enhanced multi-modal strategy, model fallback, and performance tracking."""
        # Check cache first
        prompt_hash = str(hash(prompt + task_type + str(use_multi_modal)))
        if hasattr(self, '_prompt_cache') and prompt_hash in self._prompt_cache:
            logger.info(f"Using cached result for {task_type}")
            return self._prompt_cache[prompt_hash]
        
        # Initialize cache and stats if not exists
        if not hasattr(self, '_prompt_cache'):
            self._prompt_cache = {}
        if not hasattr(self, '_model_performance_stats'):
            self._model_performance_stats = {}
        
        # Multi-modal approach for complex tasks
        if use_multi_modal and task_type in self.complex_task_routing:
            return self._generate_multi_modal(prompt, task_type, prompt_hash)
        
        # Single model approach with enhanced fallback
        preferred_model_key = self.task_models.get(task_type, 'default')
        preferred_model = self.models[preferred_model_key]
        
        # Enhanced model order based on task type and performance stats
        model_order = self._get_optimal_model_order(preferred_model, task_type)
        
        for i, model_name in enumerate(model_order):
            try:
                logger.info(f"Attempting generation with model: {model_name} for {task_type} (attempt {i+1})")
                
                # Enhanced generation parameters based on task type
                generation_params = self._get_generation_parameters(task_type)
                
                response = self.client.generate(
                    model=model_name,
                    prompt=prompt,
                    options=generation_params
                )
                
                result = response.get('response', '').strip()
                
                # Enhanced content validation
                if self._validate_generated_content(result, task_type):
                    # Cache successful result and update performance stats
                    self._prompt_cache[prompt_hash] = result
                    self._update_performance_stats(model_name, task_type, True)
                    logger.info(f"Successfully generated content with model: {model_name}")
                    return result
                else:
                    logger.warning(f"Model {model_name} returned insufficient or invalid content")
                    self._update_performance_stats(model_name, task_type, False)
                
            except Exception as e:
                logger.warning(f"Model {model_name} failed: {str(e)}")
                self._update_performance_stats(model_name, task_type, False)
                continue
        
        # Enhanced fallback content
        logger.error("All models failed, using enhanced fallback content")
        return self._generate_enhanced_fallback(task_type, prompt)
    
    def _generate_multi_modal(self, prompt: str, task_type: str, prompt_hash: str) -> str:
        """Generate content using multiple models for enhanced quality."""
        model_keys = self.complex_task_routing.get(task_type, ['primary'])
        results = []
        
        for model_key in model_keys[:2]:  # Limit to 2 models for performance
            model_name = self.models.get(model_key, self.models['primary'])
            try:
                logger.info(f"Multi-modal generation with {model_name} for {task_type}")
                
                response = self.client.generate(
                    model=model_name,
                    prompt=prompt,
                    options=self._get_generation_parameters(task_type)
                )
                
                result = response.get('response', '').strip()
                if self._validate_generated_content(result, task_type):
                    results.append(result)
                    
            except Exception as e:
                logger.warning(f"Multi-modal model {model_name} failed: {str(e)}")
                continue
        
        if results:
            # Combine and enhance results from multiple models
            combined_result = self._combine_multi_modal_results(results, task_type)
            self._prompt_cache[prompt_hash] = combined_result
            return combined_result
        else:
            # Fallback to single model approach
            return self._generate_with_fallback(prompt, task_type, use_multi_modal=False)
    
    def _get_optimal_model_order(self, preferred_model: str, task_type: str) -> List[str]:
        """Get optimal model order based on performance stats and task type."""
        # Start with preferred model
        model_order = [preferred_model]
        
        # Add high-performing models for this task type
        if hasattr(self, '_model_performance_stats'):
            task_stats = self._model_performance_stats.get(task_type, {})
            sorted_models = sorted(task_stats.items(), key=lambda x: x[1].get('success_rate', 0), reverse=True)
            for model_name, _ in sorted_models:
                if model_name not in model_order:
                    model_order.append(model_name)
        
        # Add remaining models as final fallbacks
        for model in self.models.values():
            if model not in model_order:
                model_order.append(model)
        
        return model_order
    
    def _get_generation_parameters(self, task_type: str) -> Dict[str, Any]:
        """Get optimized generation parameters based on task type."""
        base_params = {
            'temperature': 0.7,
            'top_p': 0.9,
            'num_predict': 1500
        }
        
        # Task-specific parameter optimization
        if task_type in ['technical', 'code_generation']:
            base_params.update({
                'temperature': 0.3,  # Lower temperature for more precise technical content
                'top_p': 0.8,
                'num_predict': 2000
            })
        elif task_type in ['creative', 'design']:
            base_params.update({
                'temperature': 0.8,  # Higher temperature for more creative content
                'top_p': 0.95,
                'num_predict': 1800
            })
        elif task_type in ['analysis', 'detailed']:
            base_params.update({
                'temperature': 0.5,  # Balanced temperature for analytical content
                'top_p': 0.9,
                'num_predict': 2500
            })
        
        return base_params
    
    def _validate_generated_content(self, content: str, task_type: str) -> bool:
        """Enhanced content validation based on task type."""
        if not content or len(content) < 50:
            return False
        
        # Task-specific validation
        if task_type == 'technical' and 'implementation' not in content.lower():
            return False
        elif task_type == 'design' and 'design' not in content.lower():
            return False
        elif task_type == 'ux' and 'user' not in content.lower():
            return False
        
        # General quality checks
        if content.count('Error:') > 0 or content.count('failed') > 2:
            return False
        
        return True
    
    def _update_performance_stats(self, model_name: str, task_type: str, success: bool):
        """Update model performance statistics."""
        if task_type not in self._model_performance_stats:
            self._model_performance_stats[task_type] = {}
        
        if model_name not in self._model_performance_stats[task_type]:
            self._model_performance_stats[task_type][model_name] = {
                'attempts': 0,
                'successes': 0,
                'success_rate': 0.0
            }
        
        stats = self._model_performance_stats[task_type][model_name]
        stats['attempts'] += 1
        if success:
            stats['successes'] += 1
        stats['success_rate'] = stats['successes'] / stats['attempts']
    
    def _combine_multi_modal_results(self, results: List[str], task_type: str) -> str:
        """Combine results from multiple models."""
        if len(results) == 1:
            return results[0]
        
        # For now, use the longest, most detailed result
        # In future versions, could implement sophisticated merging
        return max(results, key=len)
    
    def _generate_enhanced_fallback(self, task_type: str, original_prompt: str) -> str:
        """Generate enhanced fallback content when all models fail."""
        fallback_templates = {
            'design': """## Design Requirements
            
Based on the analyzed website, create a modern, user-friendly design with the following considerations:

**Visual Design:**
- Implement a clean, contemporary aesthetic
- Use a balanced color palette that reflects the brand personality
- Employ modern typography with good readability
- Create clear visual hierarchy to guide user attention

**Layout & Structure:**
- Design responsive layouts that work across all devices
- Implement intuitive navigation patterns
- Use appropriate spacing and white space
- Create consistent component patterns

**User Experience:**
- Focus on usability and accessibility
- Implement clear call-to-action elements
- Design for mobile-first approach
- Ensure fast loading and smooth interactions""",
            
            'technical': """## Technical Implementation Guide
            
**Frontend Technologies:**
- Modern JavaScript framework (React, Vue, or Angular)
- Responsive CSS framework (Tailwind CSS or Bootstrap)
- Build tools and bundlers (Vite, Webpack)

**Backend Requirements:**
- RESTful API design
- Database integration
- Authentication and security
- Performance optimization

**Development Best Practices:**
- Clean, maintainable code structure
- Testing framework implementation
- Version control with Git
- Deployment automation""",
            
            'functionality': """## Functionality Requirements
            
**Core Features:**
- User authentication and authorization
- Content management system
- Search and filtering capabilities
- Responsive user interface

**User Interactions:**
- Intuitive navigation flow
- Form handling and validation
- Interactive elements and feedback
- Error handling and loading states

**Business Logic:**
- Data processing and management
- User workflow optimization
- Integration with third-party services
- Analytics and tracking implementation""",
            
            'ux': """## User Experience Guidelines
            
**User-Centered Design:**
- Research target audience needs and behaviors
- Create user personas and journey maps
- Design intuitive information architecture
- Implement accessibility best practices

**Interaction Design:**
- Clear visual feedback for all actions
- Consistent interaction patterns
- Efficient task completion flows
- Error prevention and recovery

**Usability Optimization:**
- Minimize cognitive load
- Provide clear navigation paths
- Implement progressive disclosure
- Test with real users and iterate"""
        }
        
        template = fallback_templates.get(task_type, fallback_templates['design'])
        return f"**Note: AI generation unavailable. Using enhanced template.**\n\n{template}"
    
    def clear_cache(self):
        """Clear the prompt generation cache."""
        if hasattr(self, '_prompt_cache'):
            self._prompt_cache.clear()
            logger.info("Prompt cache cleared")
        
    def generate_comprehensive_prompt(self, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive prompt for recreating a similar website/application using multi-modal AI.
        
        Args:
            analysis_data (dict): Structured analysis data from WebsiteAnalyzer
            
        Returns:
            dict: Comprehensive prompt in both text and JSON formats with enhanced quality
        """
        try:
            logger.info("Generating comprehensive prompt from analysis data using multi-modal AI")
            
            # Enhanced prompt generation with multi-modal approach for better quality
            design_prompt = self._generate_design_prompt_enhanced(analysis_data)
            functionality_prompt = self._generate_functionality_prompt_enhanced(analysis_data)
            technical_prompt = self._generate_technical_prompt_enhanced(analysis_data)
            content_prompt = self._generate_content_prompt_enhanced(analysis_data)
            ux_prompt = self._generate_ux_prompt_enhanced(analysis_data)
            
            # New enhanced sections
            accessibility_prompt = self._generate_accessibility_prompt(analysis_data)
            performance_prompt = self._generate_performance_prompt(analysis_data)
            seo_prompt = self._generate_seo_prompt(analysis_data)
            
            # Combine all sections into a comprehensive prompt
            comprehensive_prompt = self._combine_prompt_sections_enhanced({
                'design': design_prompt,
                'functionality': functionality_prompt,
                'technical': technical_prompt,
                'content': content_prompt,
                'user_experience': ux_prompt,
                'accessibility': accessibility_prompt,
                'performance': performance_prompt,
                'seo': seo_prompt
            }, analysis_data)
            
            # Generate enhanced formats
            text_prompt = self._format_as_text_enhanced(comprehensive_prompt, analysis_data)
            json_prompt = self._format_as_json_enhanced(comprehensive_prompt, analysis_data)
            markdown_prompt = self._format_as_markdown(comprehensive_prompt, analysis_data)
            
            # Generate implementation roadmap
            implementation_roadmap = self._generate_implementation_roadmap(analysis_data, comprehensive_prompt)
            
            return {
                'text_format': text_prompt,
                'json_format': json_prompt,
                'markdown_format': markdown_prompt,
                'sections': comprehensive_prompt,
                'implementation_roadmap': implementation_roadmap,
                'metadata': {
                    'source_url': analysis_data.get('website_info', {}).get('url', ''),
                    'analysis_timestamp': analysis_data.get('timestamp'),
                    'website_type': analysis_data.get('website_info', {}).get('website_type', ''),
                    'primary_purpose': analysis_data.get('website_info', {}).get('primary_purpose', ''),
                    'complexity_score': self._calculate_complexity_score(analysis_data),
                    'estimated_development_time': self._estimate_development_time(analysis_data),
                    'recommended_team_size': self._recommend_team_size(analysis_data),
                    'technology_recommendations': self._recommend_technologies(analysis_data)
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
            prompt = f"SYSTEM: {system_prompt}\nUSER: {user_prompt}"
            return self._generate_with_fallback(prompt, 'design')
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
            prompt = f"SYSTEM: {system_prompt}\nUSER: {user_prompt}"
            return self._generate_with_fallback(prompt, 'functionality')
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
            prompt = f"SYSTEM: {system_prompt}\nUSER: {user_prompt}"
            return self._generate_with_fallback(prompt, 'technical')
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
            prompt = f"SYSTEM: {system_prompt}\nUSER: {user_prompt}"
            return self._generate_with_fallback(prompt, 'content')
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
            prompt = f"SYSTEM: {system_prompt}\nUSER: {user_prompt}"
            return self._generate_with_fallback(prompt, 'ux')
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
            prompt = f"SYSTEM: {system_prompt}\nUSER: {user_prompt}"
            executive_summary = self._generate_with_fallback(prompt, 'detailed')
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
        """Enhanced fallback design prompt that uses actual analysis data."""
        color_palette = design_analysis.get('color_palette', {})
        typography = design_analysis.get('typography', {})
        layout = design_analysis.get('layout', {})
        ui_components = design_analysis.get('ui_components', {})
        design_patterns = design_analysis.get('design_patterns', [])
        
        # Extract specific details from analysis
        primary_colors = color_palette.get('primary_colors', ['#333333', '#ffffff'])
        color_scheme = color_palette.get('color_scheme', 'professional')
        font_families = typography.get('font_families', ['sans-serif'])
        layout_type = layout.get('layout_type', 'modern')
        
        # Build detailed prompt based on actual data
        prompt = f"""## Design System Analysis & Recreation Guide

### Visual Identity
**Color Palette:**
- Primary colors: {', '.join(primary_colors[:5])}
- Color scheme: {color_scheme} ({color_palette.get('mood', 'balanced')} mood)
- Background: {color_palette.get('background_color', '#ffffff')}
- Text colors: {', '.join(color_palette.get('text_colors', ['#000000'])[:3])}

**Typography System:**
- Primary fonts: {', '.join(font_families[:3])}
- Typography strategy: {typography.get('typography_strategy', 'hierarchical')}
- Font pairing: {typography.get('font_pairing', 'complementary')}
- Readability score: {typography.get('readability_score', 'good')}

### Layout Architecture
**Structure Type:** {layout_type}
- Grid system: {layout.get('grid_system', 'flexible')}
- Layout pattern: {layout.get('layout_pattern', 'header-main-footer')}
- Content organization: {layout.get('content_organization', 'logical')}
- Responsive breakpoints: {layout.get('responsive_breakpoints', 'standard')}

### UI Components Detected
{chr(10).join(f"- {component}: {details}" for component, details in ui_components.items()) if ui_components else "- Standard web components"}

### Design Patterns
{chr(10).join(f"- {pattern}" for pattern in design_patterns) if design_patterns else "- Modern web design patterns"}

### Implementation Recommendations
1. Maintain consistent spacing and typography scales
2. Implement the detected color system with proper contrast ratios
3. Use CSS Grid/Flexbox for the {layout_type} layout structure
4. Ensure responsive design across all breakpoints
5. Recreate the identified UI components with modern CSS/JavaScript"""

        return prompt
    
    def _fallback_functionality_prompt(self, functionality_analysis: Dict[str, Any]) -> str:
        """Enhanced fallback functionality prompt using actual analysis data."""
        core_features = functionality_analysis.get('core_features', [])
        user_interactions = functionality_analysis.get('user_interactions', {})
        navigation_structure = functionality_analysis.get('navigation_structure', {})
        form_functionality = functionality_analysis.get('form_functionality', {})
        search_functionality = functionality_analysis.get('search_functionality', {})
        social_features = functionality_analysis.get('social_features', [])
        
        return f"""## Functionality Analysis & Implementation Guide

### Core Features Detected
{chr(10).join(f"- **{feature}**: Implement with full functionality" for feature in core_features) if core_features else "- Standard web functionality"}

### User Interaction Patterns  
**Interactive Elements:**
- Buttons: {user_interactions.get('button_count', 0)} detected
- Links: {user_interactions.get('link_count', 0)} detected
- Input fields: {user_interactions.get('input_count', 0)} detected
- Complexity level: {user_interactions.get('interaction_complexity', 'medium')}

**Requirements:**
- Implement hover states and click feedback
- Ensure keyboard accessibility for all interactive elements
- Add loading states for async operations
- Include error handling and validation

### Navigation Architecture
**Structure:** {navigation_structure.get('navigation_pattern', 'horizontal')} navigation
- Items: {navigation_structure.get('navigation_items', 0)} main sections
- Search: {'Yes' if navigation_structure.get('has_search') else 'No'}
- Breadcrumbs: {'Yes' if navigation_structure.get('has_breadcrumbs') else 'No'}

### Additional Features
{chr(10).join(f"- {feature}" for feature in social_features) if social_features else "- No additional features detected"}

### Implementation Priorities
1. Core Features: Implement the {len(core_features)} main features first
2. Navigation: Build the {navigation_structure.get('navigation_pattern', 'horizontal')} navigation system  
3. Interactions: Add responsive feedback for all {user_interactions.get('button_count', 0)} interactive elements
4. Progressive Enhancement: Start with basic functionality, add advanced features"""
    
    def _fallback_technical_prompt(self, technical_analysis: Dict[str, Any]) -> str:
        """Enhanced fallback technical prompt using comprehensive analysis data."""
        frontend_tech = technical_analysis.get('frontend_technologies', [])
        modern_features = technical_analysis.get('modern_features', [])
        frameworks = technical_analysis.get('frameworks_detected', {})
        performance = technical_analysis.get('performance_metrics', {})
        architecture = technical_analysis.get('architecture_patterns', [])
        security = technical_analysis.get('security_features', {})
        
        # Build specific recommendations based on detected technologies
        framework_rec = ""
        if frameworks.get('primary_framework') != 'vanilla':
            framework_rec = f"\n**Primary Framework**: {frameworks.get('primary_framework', 'React/Vue/Angular')}"
            if frameworks.get('ecosystem'):
                framework_rec += f"\n**Ecosystem**: {frameworks.get('ecosystem')} with associated tooling"
        
        architecture_rec = ""
        if architecture:
            arch_patterns = ', '.join(architecture)
            architecture_rec = f"\n**Architecture**: Implement {arch_patterns} patterns"
        
        return f"""## Technical Implementation Requirements

**Technology Stack Recommendations:**
{chr(10).join(f'- {tech}' for tech in frontend_tech) if frontend_tech else '- HTML5, CSS3, Vanilla JavaScript'}
{framework_rec}

**Modern Web Features:**
{chr(10).join(f'- {feature.replace("_", " ").title()}' for feature in modern_features) if modern_features else '- Responsive Design\n- Progressive Enhancement\n- Semantic HTML'}

**Performance Requirements:**
- Target load time: {performance.get('load_time', 3)} seconds or less
- Implement {performance.get('optimization_level', 'standard')} optimization level
- Use {technical_analysis.get('optimization_patterns', {}).get('caching_strategy', 'browser caching')}
- Asset optimization: {'enabled' if technical_analysis.get('optimization_patterns', {}).get('asset_optimization') else 'implement compression and minification'}

**Security Implementation:**
- HTTPS enforcement: {'implemented' if security.get('https_usage') else 'required'}
- Content Security Policy: {'detected' if security.get('csp_headers') else 'implement'}
- XSS protection: {'active' if security.get('xss_protection') else 'required'}

**Browser Support Strategy:**
- Target: {technical_analysis.get('browser_support', {}).get('modern_browsers', 'Modern browsers (last 2 versions)')}
- Polyfills: {'included' if technical_analysis.get('browser_support', {}).get('polyfill_usage') else 'add as needed'}
- Progressive enhancement: {'implemented' if technical_analysis.get('browser_support', {}).get('progressive_enhancement') else 'required'}

**Development Tools:**
- Build tools: {', '.join(technical_analysis.get('build_tools', ['Webpack/Vite']))}
- Deployment: {technical_analysis.get('deployment_indicators', {}).get('deployment_type', 'Static/CDN deployment')}
{architecture_rec}

**Code Quality Standards:**
- CSS Methodology: {technical_analysis.get('code_quality', {}).get('css_methodology', 'BEM or Utility-first')}
- Semantic HTML: {technical_analysis.get('code_quality', {}).get('semantic_html', 'Required')} compliance
- Maintainability: {technical_analysis.get('code_quality', {}).get('maintainability', 'High')} standard

**API Integration:**
{f"- REST API integration: {technical_analysis.get('api_integrations', {}).get('rest_api_usage', 'Not detected')}" if technical_analysis.get('api_integrations') else '- API integration as needed'}
{f"- GraphQL usage: {technical_analysis.get('api_integrations', {}).get('graphql_usage', 'Not detected')}" if technical_analysis.get('api_integrations', {}).get('graphql_usage') else ''}
{f"- Third-party APIs: {", ".join(technical_analysis.get("api_integrations", {}).get("third_party_apis", []))}" if technical_analysis.get('api_integrations', {}).get('third_party_apis') else ''}

**Accessibility Implementation:**
- ARIA patterns: {technical_analysis.get('accessibility_implementation', {}).get('aria_usage', {}).get('aria_labels', 'Implement')}
- Keyboard navigation: {technical_analysis.get('accessibility_implementation', {}).get('keyboard_navigation', 'Full support required')}
- Screen reader support: {technical_analysis.get('accessibility_implementation', {}).get('screen_reader_support', 'Comprehensive')}
- Color contrast: {technical_analysis.get('accessibility_implementation', {}).get('color_contrast', 'WCAG AA compliant')}"""
    
    def _fallback_content_prompt(self, content_analysis: Dict[str, Any]) -> str:
        """Enhanced fallback content prompt using comprehensive analysis data."""
        content_structure = content_analysis.get('content_structure', {})
        content_types = content_analysis.get('content_types', [])
        multimedia_usage = content_analysis.get('multimedia_usage', {})
        information_architecture = content_analysis.get('information_architecture', {})
        
        return f"""## Content Strategy & Information Architecture

### Content Structure Analysis
**Content Organization:**
- Density level: {content_structure.get('content_density', 'medium')} content density
- Structure type: {content_structure.get('structure_type', 'hierarchical')} organization
- Average word count: {content_structure.get('word_count', 500)} words per page
- Content depth: {content_structure.get('content_depth', 'moderate')} complexity

### Content Types Identified
{chr(10).join(f'- **{content_type.replace("_", " ").title()}**: Essential for user engagement' for content_type in content_types) if content_types else '- Text content\n- Visual content\n- Interactive elements'}

### Information Architecture
**Navigation Structure:**
- Hierarchy depth: {information_architecture.get('hierarchy_depth', 3)} levels
- Content categorization: {information_architecture.get('categorization', 'logical')}
- User flow: {information_architecture.get('user_flow', 'linear')} progression
- Content discovery: {information_architecture.get('discovery_method', 'navigation-based')}

### Multimedia Integration Strategy
**Visual Content:**
- Image usage: {multimedia_usage.get('image_count', 'moderate')} implementation
- Video content: {'Present' if multimedia_usage.get('has_video') else 'Consider adding'}
- Interactive media: {'Detected' if multimedia_usage.get('interactive_media') else 'Optional enhancement'}
- Gallery features: {'Implemented' if multimedia_usage.get('has_gallery') else 'Not present'}

### Content Presentation Guidelines
**Writing Style:**
- Tone: {content_analysis.get('content_tone', 'professional')}
- Reading level: {content_analysis.get('reading_level', 'general audience')}
- Content format: {content_analysis.get('content_format', 'mixed media')}

**Content Hierarchy:**
1. **Primary Content**: {content_structure.get('primary_content_type', 'Main informational content')}
2. **Secondary Content**: {content_structure.get('secondary_content_type', 'Supporting details and context')}
3. **Tertiary Content**: {content_structure.get('tertiary_content_type', 'Additional resources and links')}

### Content Management Requirements
**Organization Principles:**
- Use clear headings with {information_architecture.get('heading_levels', 3)}-level hierarchy
- Implement logical content flow with clear progression
- Include relevant multimedia elements for engagement
- Ensure content supports primary user goals and objectives
- Maintain consistent voice and tone throughout

**SEO Content Strategy:**
- Target keyword density: {content_analysis.get('keyword_density', 'natural')}
- Content freshness: {content_analysis.get('content_freshness', 'regular updates recommended')}
- Internal linking: {content_analysis.get('internal_linking', 'strategic implementation')}

**Accessibility Considerations:**
- Alt text for all images and media
- Clear and descriptive headings
- Logical reading order
- Plain language principles where appropriate"""
    
    def _fallback_ux_prompt(self, ux_analysis: Dict[str, Any]) -> str:
        """Enhanced fallback UX prompt using comprehensive analysis data."""
        user_journey = ux_analysis.get('user_journey', {})
        mobile_experience = ux_analysis.get('mobile_experience', {})
        accessibility_features = ux_analysis.get('accessibility_features', {})
        conversion_optimization = ux_analysis.get('conversion_optimization', {})
        interaction_design = ux_analysis.get('interaction_design', {})
        
        return f"""## User Experience Strategy & Implementation Guide

### User Journey Mapping
**Entry Points Analysis:**
- Primary entry: {', '.join(user_journey.get('entry_points', ['homepage']))}
- User intent: {user_journey.get('primary_intent', 'information seeking')}
- Journey complexity: {user_journey.get('journey_complexity', 'simple')} user flow

**Conversion Funnel:**
- Conversion points: {', '.join(user_journey.get('conversion_points', ['contact form']))}
- Funnel stages: {user_journey.get('funnel_stages', 3)} main steps
- Drop-off prevention: {user_journey.get('retention_strategy', 'Clear CTAs and progress indicators')}

### Mobile User Experience
**Mobile Optimization:**
- Responsive design: {'Implemented' if mobile_experience.get('mobile_responsive') else 'Required'}
- Mobile-first approach: {mobile_experience.get('mobile_optimization', 'Recommended')}
- Touch interface: {'Optimized' if mobile_experience.get('touch_optimized') else 'Implement finger-friendly targets'}
- Mobile performance: {mobile_experience.get('mobile_performance', 'Optimize for 3G networks')}

**Cross-Device Experience:**
- Continuity: {mobile_experience.get('cross_device_continuity', 'Maintain consistent experience')}
- Adaptive layout: {mobile_experience.get('adaptive_features', 'Context-aware adjustments')}

### Accessibility & Inclusive Design
**WCAG Compliance:**
- Current level: {accessibility_features.get('accessibility_score', 'AA target')}
- Keyboard navigation: {accessibility_features.get('keyboard_support', 'Full support required')}
- Screen reader support: {accessibility_features.get('screen_reader', 'Comprehensive compatibility')}
- Color contrast: {accessibility_features.get('contrast_ratio', 'WCAG AA minimum')}

**Assistive Technology Support:**
- ARIA implementation: {'Present' if accessibility_features.get('aria_usage') else 'Implement comprehensive ARIA labels'}
- Focus management: {accessibility_features.get('focus_management', 'Logical tab order required')}
- Alternative content: {accessibility_features.get('alt_content', 'All media needs alternatives')}

### Interaction Design Patterns
**Micro-Interactions:**
- Feedback systems: {interaction_design.get('feedback_patterns', 'Visual and auditory confirmation')}
- Loading states: {interaction_design.get('loading_patterns', 'Progressive loading with indicators')}
- Error handling: {interaction_design.get('error_handling', 'Graceful error recovery')}
- Success states: {interaction_design.get('success_patterns', 'Clear completion feedback')}

**Animation & Transitions:**
- Animation philosophy: {interaction_design.get('animation_style', 'Subtle and purposeful')}
- Transition timing: {interaction_design.get('transition_duration', '200-300ms standard')}
- Reduced motion: {interaction_design.get('reduced_motion', 'Respect user preferences')}

### Conversion Optimization Strategy
**Conversion Elements:**
- CTA effectiveness: {conversion_optimization.get('cta_performance', 'Prominent and action-oriented')}
- Form optimization: {conversion_optimization.get('form_optimization', 'Minimize friction and fields')}
- Trust signals: {conversion_optimization.get('trust_elements', 'Social proof and security indicators')}
- Value proposition: {conversion_optimization.get('value_communication', 'Clear and compelling messaging')}

**User Engagement:**
- Engagement patterns: {conversion_optimization.get('engagement_strategy', 'Progressive disclosure')}
- Personalization: {conversion_optimization.get('personalization', 'Contextual content adaptation')}
- Retention hooks: {conversion_optimization.get('retention_features', 'Value-driven return incentives')}

### Performance & Usability Standards
**Core UX Metrics:**
- Page load perception: {ux_analysis.get('performance_perception', 'Sub-3 second perceived load')}
- Interaction responsiveness: {ux_analysis.get('interaction_speed', 'Immediate feedback (<100ms)')}
- Navigation efficiency: {ux_analysis.get('navigation_efficiency', 'Maximum 3-click rule')}

**Testing & Validation:**
- User testing approach: {ux_analysis.get('testing_strategy', 'Iterative usability testing')}
- A/B testing priorities: {ux_analysis.get('ab_testing', 'Conversion points and navigation')}
- Analytics implementation: {ux_analysis.get('analytics_tracking', 'Comprehensive user behavior tracking')}

### Implementation Priorities
1. **Foundation**: Responsive layout and basic accessibility
2. **Core Journey**: Primary user flow optimization  
3. **Conversion**: CTA placement and form optimization
4. **Enhancement**: Micro-interactions and advanced features
5. **Testing**: User feedback integration and iterative improvement"""
    
    def _fallback_executive_summary(self, website_info: Dict[str, Any], business_model: Dict[str, Any]) -> str:
        """Enhanced fallback executive summary using comprehensive analysis data."""
        website_type = website_info.get('website_type', 'modern web application')
        primary_purpose = website_info.get('primary_purpose', 'digital presence')
        target_audience = website_info.get('target_audience', 'target users')
        industry = website_info.get('industry_category', 'digital services')
        business_type = business_model.get('business_type', 'service-based')
        monetization = business_model.get('monetization_strategy', [])
        value_prop = business_model.get('value_proposition', 'comprehensive solution')
        
        return f"""## Project Executive Summary

### Project Vision & Scope
**Objective**: Create a high-quality {website_type} that serves as {primary_purpose} for {target_audience} in the {industry} sector.

**Business Context:**
- Industry: {industry.replace('_', ' ').title()}
- Business model: {business_type.replace('_', ' ').title()}
- Value proposition: {value_prop}
{f"- Monetization strategy: {', '.join(monetization)}" if monetization else "- Revenue model: To be defined based on business goals"}

### Target Audience Analysis
**Primary Users:** {target_audience}
- User intent: {website_info.get('user_intent', 'Seeking information and services')}
- Technical proficiency: {website_info.get('technical_level', 'Mixed skill levels')}
- Device preferences: {website_info.get('device_usage', 'Multi-device usage')}

### Core Requirements Summary
**Functional Requirements:**
1. **Primary Features**: Implement core {primary_purpose} functionality
2. **User Experience**: Intuitive navigation and interaction design
3. **Performance**: Fast loading times and responsive design
4. **Accessibility**: WCAG 2.1 AA compliance for inclusive access
5. **Security**: Industry-standard security measures and data protection

**Technical Requirements:**
- Modern web development stack with future-proof technologies
- Responsive design supporting all device types and screen sizes
- SEO optimization for search engine visibility
- Cross-browser compatibility and progressive enhancement
- Scalable architecture supporting business growth

**Design Requirements:**
- Professional visual design aligned with brand identity
- Consistent design system and component library
- User-centered interface design with clear information hierarchy
- Brand-appropriate color palette and typography choices
- Mobile-first responsive design approach

### Implementation Strategy
**Development Approach:**
- Agile/iterative development methodology
- Component-based architecture for maintainability
- Progressive enhancement starting with core functionality
- Continuous testing and user feedback integration

**Quality Assurance:**
- Comprehensive cross-browser and device testing
- Performance optimization and monitoring
- Accessibility testing and compliance verification
- Security auditing and vulnerability assessment
- User acceptance testing and feedback incorporation

**Deployment & Maintenance:**
- Modern deployment pipeline with version control
- Content management system for easy updates
- Performance monitoring and analytics integration
- Regular security updates and maintenance schedule
- Scalable hosting solution supporting traffic growth

### Success Metrics & KPIs
**Performance Indicators:**
- Page load time: Target <3 seconds
- Mobile performance: Core Web Vitals compliance
- Accessibility: WCAG 2.1 AA certification
- User engagement: Improved bounce rate and session duration
- Conversion: Enhanced user goal completion rates

**Business Outcomes:**
- Increased {target_audience} engagement and satisfaction
- Enhanced brand presence and professional credibility
- Improved operational efficiency through digital transformation
- Measurable ROI through {primary_purpose} optimization
- Scalable foundation for future business growth

### Risk Mitigation
**Technical Risks:**
- Browser compatibility through progressive enhancement
- Performance issues via optimization and monitoring
- Security vulnerabilities through best practices and auditing
- Scalability concerns via cloud-based infrastructure

**Project Risks:**
- Scope creep through clear requirements documentation
- Timeline delays via agile methodology and regular check-ins
- Budget overruns through phased development approach
- User adoption via comprehensive testing and feedback integration"""

    # Enhanced Prompt Generation Methods
    
    def _generate_design_prompt_enhanced(self, analysis_data: Dict[str, Any]) -> str:
        """Generate enhanced design-focused prompt using multi-modal AI."""
        design_analysis = analysis_data.get('design_analysis', {})
        
        system_prompt = """You are an expert UI/UX designer with deep knowledge of modern design principles, accessibility standards, and current design trends. Based on the comprehensive website analysis provided, generate a detailed, actionable design prompt that captures not just the visual elements, but the design philosophy, user psychology, and strategic design decisions."""
        
        enhanced_prompt = f"""
        Based on this comprehensive website analysis, create a detailed design implementation guide:
        
        **Advanced Design Analysis:**
        - Color Psychology: {design_analysis.get('color_palette', {}).get('psychology_profile', {})}
        - Typography Intelligence: {design_analysis.get('typography', {})}
        - Layout Sophistication: {design_analysis.get('layout', {})}
        - Design System Maturity: {design_analysis.get('design_system', {})}
        - Brand Personality: {design_analysis.get('brand_analysis', {})}
        - Visual Style Profile: {design_analysis.get('visual_style', {})}
        - Accessibility Features: {design_analysis.get('accessibility', {})}
        - Modern Design Trends: {design_analysis.get('design_trends', [])}
        
        Generate a comprehensive design guide covering:
        
        1. **Design Philosophy & Strategy**
           - Overall aesthetic direction and design principles
           - Target audience design considerations
           - Brand alignment and visual identity strategy
           - Emotional design goals and user psychology
        
        2. **Advanced Color System**
           - Primary, secondary, and accent color specifications
           - Color harmony and psychological impact
           - Dark mode and accessibility considerations
           - Semantic color usage (success, warning, error states)
        
        3. **Sophisticated Typography System**
           - Font pairing strategy and hierarchy implementation
           - Readability optimization across devices
           - Brand personality expression through typography
           - Performance and loading considerations
        
        4. **Layout & Spatial Design**
           - Grid system and spacing rhythm
           - Modern CSS layout techniques (Grid, Flexbox)
           - Responsive breakpoint strategy
           - Component composition and reusability
        
        5. **Interactive Design Elements**
           - Button system with variants and states
           - Form design and input patterns
           - Navigation and menu systems
           - Card layouts and content containers
        
        6. **Motion & Animation Strategy**
           - Micro-interaction design principles
           - Page transition and loading animations
           - Accessibility considerations for motion
           - Performance optimization for animations
        
        Provide specific implementation details and modern CSS techniques.
        """
        
        try:
            return self._generate_with_fallback(
                f"SYSTEM: {system_prompt}\nUSER: {enhanced_prompt}", 
                'design', 
                use_multi_modal=True
            )
        except Exception as e:
            logger.error(f"Error generating enhanced design prompt: {str(e)}")
            return self._fallback_design_prompt(design_analysis)
    
    def _generate_functionality_prompt_enhanced(self, analysis_data: Dict[str, Any]) -> str:
        """Generate enhanced functionality-focused prompt using specialized models."""
        functionality_analysis = analysis_data.get('functionality_analysis', {})
        
        system_prompt = """You are a senior software architect and product manager with expertise in modern web applications, user experience design, and technical implementation. Generate a comprehensive functionality specification that covers both user-facing features and technical implementation details."""
        
        enhanced_prompt = f"""
        Based on this detailed functionality analysis, create a comprehensive feature specification:
        
        **Functionality Intelligence:**
        - Core Features: {functionality_analysis.get('core_features', [])}
        - User Interactions: {functionality_analysis.get('user_interactions', {})}
        - Navigation Architecture: {functionality_analysis.get('navigation_structure', {})}
        - Form Systems: {functionality_analysis.get('form_functionality', {})}
        - Search & Discovery: {functionality_analysis.get('search_functionality', {})}
        - Social Features: {functionality_analysis.get('social_features', [])}
        - Advanced Capabilities: {functionality_analysis.get('advanced_features', [])}
        
        Generate a detailed implementation guide covering:
        
        1. **Core Feature Architecture**
           - Primary user flows and use cases
           - Feature prioritization and MVP definition
           - Advanced functionality roadmap
           - Integration points and dependencies
        
        2. **User Interaction Patterns**
           - Interactive component specifications
           - State management and data flow
           - Real-time features and notifications
           - Offline capability requirements
        
        3. **Navigation & Information Architecture**
           - Site structure and content organization
           - Search functionality and filtering
           - Breadcrumb and wayfinding systems
           - Mobile navigation patterns
        
        4. **Data Management & Forms**
           - Form validation and error handling
           - Data persistence and synchronization
           - File upload and media management
           - User preferences and settings
        
        5. **Advanced Features & Integrations**
           - Third-party service integrations
           - API design and data exchange
           - Analytics and tracking implementation
           - Performance monitoring and optimization
        
        6. **Security & Compliance**
           - Authentication and authorization flows
           - Data protection and privacy compliance
           - Input sanitization and security measures
           - Audit trails and logging systems
        
        Include technical implementation details and modern best practices.
        """
        
        try:
            return self._generate_with_fallback(
                f"SYSTEM: {system_prompt}\nUSER: {enhanced_prompt}", 
                'functionality', 
                use_multi_modal=True
            )
        except Exception as e:
            logger.error(f"Error generating enhanced functionality prompt: {str(e)}")
            return self._fallback_functionality_prompt(functionality_analysis)
    
    def _generate_technical_prompt_enhanced(self, analysis_data: Dict[str, Any]) -> str:
        """Generate enhanced technical implementation prompt using code-specialized models."""
        technical_analysis = analysis_data.get('technical_analysis', {})
        
        system_prompt = """You are a lead developer and DevOps engineer with expertise in modern web technologies, cloud architecture, and performance optimization. Generate a comprehensive technical implementation guide that covers architecture, technologies, deployment, and maintenance."""
        
        enhanced_prompt = f"""
        Based on this technical analysis, create a detailed implementation specification:
        
        **Technical Intelligence:**
        - Frontend Technologies: {technical_analysis.get('frontend_technologies', [])}
        - Backend Architecture: {technical_analysis.get('backend_analysis', {})}
        - Modern Features: {technical_analysis.get('modern_features', [])}
        - Performance Metrics: {technical_analysis.get('performance_analysis', {})}
        - Security Implementation: {technical_analysis.get('security_analysis', {})}
        - Deployment Strategy: {technical_analysis.get('deployment_analysis', {})}
        
        Generate a comprehensive technical guide covering:
        
        1. **Architecture & Technology Stack**
           - Frontend framework selection and justification
           - Backend technology and database choices
           - Microservices vs monolithic considerations
           - Cloud platform and hosting strategy
        
        2. **Development Environment & Tools**
           - Build system and bundler configuration
           - Code quality tools and linting setup
           - Testing framework and coverage requirements
           - Development workflow and CI/CD pipeline
        
        3. **Performance Optimization**
           - Core Web Vitals optimization strategies
           - Code splitting and lazy loading implementation
           - Asset optimization and CDN strategy
           - Database query optimization and caching
        
        4. **Security Implementation**
           - Authentication and authorization systems
           - Data encryption and secure communication
           - Input validation and sanitization
           - Security headers and OWASP compliance
        
        5. **Scalability & Monitoring**
           - Auto-scaling and load balancing setup
           - Error tracking and performance monitoring
           - Logging and analytics implementation
           - Backup and disaster recovery planning
        
        6. **Maintenance & Operations**
           - Version control and release management
           - Documentation and code commenting standards
           - Team collaboration and code review processes
           - Long-term maintenance and technical debt management
        
        Provide specific implementation code examples and configuration details.
        """
        
        try:
            return self._generate_with_fallback(
                f"SYSTEM: {system_prompt}\nUSER: {enhanced_prompt}", 
                'technical', 
                use_multi_modal=True
            )
        except Exception as e:
            logger.error(f"Error generating enhanced technical prompt: {str(e)}")
            return self._fallback_technical_prompt(technical_analysis)
    
    def _generate_content_prompt_enhanced(self, analysis_data: Dict[str, Any]) -> str:
        """Generate enhanced content strategy prompt using conversational AI."""
        content_analysis = analysis_data.get('content_strategy', {})
        
        system_prompt = """You are a content strategist and UX writer with expertise in information architecture, SEO, and user-centered content design. Generate a comprehensive content strategy that addresses both user needs and business objectives."""
        
        enhanced_prompt = f"""
        Based on this content analysis, create a detailed content implementation strategy:
        
        **Content Intelligence:**
        - Content Structure: {content_analysis.get('content_structure', {})}
        - Content Types: {content_analysis.get('content_types', [])}
        - Information Architecture: {content_analysis.get('information_architecture', {})}
        - SEO Analysis: {content_analysis.get('seo_analysis', {})}
        - Multimedia Usage: {content_analysis.get('multimedia_usage', {})}
        - Content Quality: {content_analysis.get('content_quality', {})}
        
        Generate a comprehensive content guide covering:
        
        1. **Content Strategy & Governance**
           - Content mission and editorial guidelines
           - Voice, tone, and brand personality
           - Content lifecycle and maintenance processes
           - Quality assurance and review workflows
        
        2. **Information Architecture**
           - Content hierarchy and organization
           - Navigation and findability strategies
           - Search functionality and content discovery
           - Cross-linking and content relationships
        
        3. **Content Creation Guidelines**
           - Writing style and formatting standards
           - Accessibility and inclusive language practices
           - SEO optimization and keyword strategy
           - Multimedia content integration standards
        
        4. **User Experience Content**
           - Microcopy and interface text guidelines
           - Error messages and help documentation
           - Onboarding and tutorial content
           - Form labels and instructional text
        
        5. **Content Management & Workflows**
           - Content creation and approval processes
           - Publishing schedules and content calendars
           - Version control and content updates
           - Analytics and performance measurement
        
        6. **Localization & Accessibility**
           - Multi-language content considerations
           - Cultural adaptation and localization
           - Screen reader compatibility
           - Plain language and readability optimization
        
        Include specific examples and implementation guidelines.
        """
        
        try:
            return self._generate_with_fallback(
                f"SYSTEM: {system_prompt}\nUSER: {enhanced_prompt}", 
                'content', 
                use_multi_modal=True
            )
        except Exception as e:
            logger.error(f"Error generating enhanced content prompt: {str(e)}")
            return self._fallback_content_prompt(content_analysis)
    
    def _generate_ux_prompt_enhanced(self, analysis_data: Dict[str, Any]) -> str:
        """Generate enhanced UX strategy prompt using detailed analysis."""
        ux_analysis = analysis_data.get('user_experience_analysis', {})
        
        system_prompt = """You are a UX research expert and interaction designer with deep knowledge of user psychology, accessibility principles, and conversion optimization. Generate a comprehensive UX strategy that prioritizes user needs while achieving business objectives."""
        
        enhanced_prompt = f"""
        Based on this UX analysis, create a detailed user experience strategy:
        
        **UX Intelligence:**
        - User Journey: {ux_analysis.get('user_journey', {})}
        - Usability Patterns: {ux_analysis.get('usability_patterns', {})}
        - Accessibility Features: {ux_analysis.get('accessibility_features', {})}
        - Mobile Experience: {ux_analysis.get('mobile_experience', {})}
        - Conversion Optimization: {ux_analysis.get('conversion_optimization', {})}
        - User Research Insights: {ux_analysis.get('user_research', {})}
        
        Generate a comprehensive UX implementation guide covering:
        
        1. **User Research & Personas**
           - Target user identification and segmentation
           - User journey mapping and pain point analysis
           - Accessibility and inclusive design considerations
           - Usability testing and validation strategies
        
        2. **Interaction Design Patterns**
           - Micro-interaction design and feedback systems
           - Navigation patterns and wayfinding
           - Form design and input optimization
           - Error prevention and recovery strategies
        
        3. **Mobile & Responsive Experience**
           - Mobile-first design principles
           - Touch interface optimization
           - Progressive web app considerations
           - Cross-device experience continuity
        
        4. **Accessibility & Inclusion**
           - WCAG 2.1 AA compliance implementation
           - Keyboard navigation and focus management
           - Screen reader optimization
           - Color contrast and visual accessibility
        
        5. **Conversion & Engagement**
           - Call-to-action optimization
           - Trust building and social proof elements
           - Onboarding and user activation flows
           - Retention and re-engagement strategies
        
        6. **Testing & Optimization**
           - A/B testing framework and metrics
           - User feedback collection and analysis
           - Performance monitoring and optimization
           - Continuous improvement processes
        
        Provide actionable recommendations and implementation priorities.
        """
        
        try:
            return self._generate_with_fallback(
                f"SYSTEM: {system_prompt}\nUSER: {enhanced_prompt}", 
                'ux', 
                use_multi_modal=True
            )
        except Exception as e:
            logger.error(f"Error generating enhanced UX prompt: {str(e)}")
            return self._fallback_ux_prompt(ux_analysis)
    
    # New enhanced prompt sections
    
    def _generate_accessibility_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Generate comprehensive accessibility implementation prompt."""
        accessibility_analysis = analysis_data.get('design_analysis', {}).get('accessibility', {})
        
        prompt = f"""
        Generate a comprehensive accessibility implementation strategy:
        
        Current Accessibility Assessment: {accessibility_analysis}
        
        **Implementation Requirements:**
        1. WCAG 2.1 AA compliance standards
        2. Screen reader optimization and ARIA implementation
        3. Keyboard navigation and focus management
        4. Color contrast and visual accessibility
        5. Mobile accessibility considerations
        6. Testing and validation procedures
        """
        
        try:
            return self._generate_with_fallback(prompt, 'accessibility')
        except Exception:
            return """## Accessibility Implementation Strategy
            
**WCAG 2.1 AA Compliance:**
- Implement semantic HTML structure with proper heading hierarchy
- Ensure sufficient color contrast ratios (4.5:1 for normal text)
- Provide alternative text for all images and multimedia content
- Design keyboard-accessible navigation and interactive elements

**Screen Reader Optimization:**
- Use ARIA labels and descriptions for complex components
- Implement proper form labeling and error messaging
- Provide skip navigation links and landmark regions
- Test with actual screen reader software

**Testing & Validation:**
- Automated accessibility testing integration
- Manual testing with assistive technologies
- User testing with disabled users
- Regular accessibility audits and compliance monitoring"""
    
    def _generate_performance_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Generate performance optimization prompt."""
        performance_analysis = analysis_data.get('technical_analysis', {}).get('performance_analysis', {})
        
        prompt = f"""
        Generate a comprehensive performance optimization strategy:
        
        Current Performance Metrics: {performance_analysis}
        
        **Optimization Requirements:**
        1. Core Web Vitals optimization (LCP, FID, CLS)
        2. Asset optimization and delivery strategies
        3. Code splitting and lazy loading implementation
        4. Caching strategies and CDN utilization
        5. Database and API optimization
        6. Monitoring and measurement frameworks
        """
        
        try:
            return self._generate_with_fallback(prompt, 'technical')
        except Exception:
            return """## Performance Optimization Strategy
            
**Core Web Vitals:**
- Largest Contentful Paint (LCP): Target <2.5 seconds
- First Input Delay (FID): Target <100 milliseconds
- Cumulative Layout Shift (CLS): Target <0.1

**Asset Optimization:**
- Image compression and next-gen formats (WebP, AVIF)
- CSS and JavaScript minification and compression
- Critical CSS inlining and non-critical resource deferring
- Font optimization and loading strategies

**Code Performance:**
- Bundle splitting and dynamic imports
- Tree shaking and dead code elimination
- Service worker implementation for caching
- Database query optimization and indexing"""
    
    def _generate_seo_prompt(self, analysis_data: Dict[str, Any]) -> str:
        """Generate SEO optimization prompt."""
        seo_analysis = analysis_data.get('content_strategy', {}).get('seo_analysis', {})
        
        prompt = f"""
        Generate a comprehensive SEO implementation strategy:
        
        Current SEO Analysis: {seo_analysis}
        
        **SEO Requirements:**
        1. Technical SEO optimization and site structure
        2. Content strategy and keyword optimization
        3. Meta tag and structured data implementation
        4. Site speed and Core Web Vitals for SEO
        5. Mobile-first indexing considerations
        6. Local SEO and schema markup
        """
        
        try:
            return self._generate_with_fallback(prompt, 'content')
        except Exception:
            return """## SEO Implementation Strategy
            
**Technical SEO:**
- Implement proper URL structure and canonical tags
- Create XML sitemaps and robots.txt optimization
- Ensure proper heading hierarchy (H1-H6) usage
- Implement structured data and schema markup

**Content Optimization:**
- Keyword research and content strategy development
- Meta title and description optimization
- Internal linking strategy and anchor text optimization
- Content freshness and regular updates

**Performance & Mobile:**
- Core Web Vitals optimization for ranking factors
- Mobile-first design and responsive implementation
- Site speed optimization and loading performance
- Progressive web app features for enhanced UX"""
    
    # Enhanced formatting and utility methods
    
    def _combine_prompt_sections_enhanced(self, sections: Dict[str, str], analysis_data: Dict[str, Any]) -> Dict[str, str]:
        """Combine prompt sections with enhanced organization and flow."""
        website_info = analysis_data.get('website_info', {})
        business_model = analysis_data.get('business_model', {})
        
        # Generate executive summary using multi-modal approach
        executive_summary = self._generate_executive_summary_enhanced(website_info, business_model)
        
        enhanced_sections = {
            'executive_summary': executive_summary,
            'design': sections.get('design', ''),
            'functionality': sections.get('functionality', ''),
            'technical': sections.get('technical', ''),
            'content': sections.get('content', ''),
            'user_experience': sections.get('user_experience', ''),
            'accessibility': sections.get('accessibility', ''),
            'performance': sections.get('performance', ''),
            'seo': sections.get('seo', ''),
            'implementation_roadmap': self._generate_implementation_roadmap(analysis_data, sections)
        }
        
        return enhanced_sections
    
    def _format_as_text_enhanced(self, sections: Dict[str, str], analysis_data: Dict[str, Any]) -> str:
        """Format prompt sections as enhanced readable text."""
        website_url = analysis_data.get('website_info', {}).get('url', 'analyzed website')
        website_type = analysis_data.get('website_info', {}).get('website_type', 'web application')
        
        text_prompt = f"""# Website Recreation Prompt - Enhanced Analysis
        
**Source:** {website_url}
**Type:** {website_type.replace('_', ' ').title()}
**Generated:** {analysis_data.get('timestamp', 'Unknown')}

---

{sections.get('executive_summary', '')}

---

{sections.get('design', '')}

---

{sections.get('functionality', '')}

---

{sections.get('technical', '')}

---

{sections.get('content', '')}

---

{sections.get('user_experience', '')}

---

{sections.get('accessibility', '')}

---

{sections.get('performance', '')}

---

{sections.get('seo', '')}

---

{sections.get('implementation_roadmap', '')}

---

## Additional Notes

This comprehensive prompt was generated using advanced AI analysis with multiple specialized models for different aspects of web development. Each section provides detailed, actionable guidance for recreating a similar website or application.

**Recommended Approach:**
1. Start with the executive summary for project context
2. Follow the implementation roadmap for structured development
3. Use each section as a detailed specification for that aspect
4. Adapt recommendations based on your specific requirements and constraints

**Quality Assurance:**
- Cross-reference requirements between sections
- Validate design decisions against user experience guidelines
- Ensure technical choices support business objectives
- Test accessibility and performance throughout development
"""
        
        return text_prompt.strip()
    
    def _format_as_json_enhanced(self, sections: Dict[str, str], analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format prompt sections as enhanced structured JSON."""
        return {
            "metadata": {
                "source_url": analysis_data.get('website_info', {}).get('url', ''),
                "website_type": analysis_data.get('website_info', {}).get('website_type', ''),
                "analysis_timestamp": analysis_data.get('timestamp', ''),
                "prompt_version": "2.0_enhanced",
                "ai_models_used": list(self.models.keys()),
                "complexity_score": self._calculate_complexity_score(analysis_data),
                "estimated_effort": self._estimate_development_time(analysis_data)
            },
            "project_overview": {
                "executive_summary": sections.get('executive_summary', ''),
                "key_objectives": self._extract_key_objectives(analysis_data),
                "success_criteria": self._define_success_criteria(analysis_data),
                "risk_factors": self._identify_risk_factors(analysis_data)
            },
            "specifications": {
                "design": {
                    "content": sections.get('design', ''),
                    "priority": "high",
                    "dependencies": ["user_experience"],
                    "estimated_effort": "3-4 weeks"
                },
                "functionality": {
                    "content": sections.get('functionality', ''),
                    "priority": "critical",
                    "dependencies": ["technical", "design"],
                    "estimated_effort": "4-6 weeks"
                },
                "technical": {
                    "content": sections.get('technical', ''),
                    "priority": "critical",
                    "dependencies": [],
                    "estimated_effort": "2-3 weeks"
                },
                "content": {
                    "content": sections.get('content', ''),
                    "priority": "medium",
                    "dependencies": ["design", "functionality"],
                    "estimated_effort": "2-3 weeks"
                },
                "user_experience": {
                    "content": sections.get('user_experience', ''),
                    "priority": "high",
                    "dependencies": ["design"],
                    "estimated_effort": "2-3 weeks"
                },
                "accessibility": {
                    "content": sections.get('accessibility', ''),
                    "priority": "high",
                    "dependencies": ["design", "functionality"],
                    "estimated_effort": "1-2 weeks"
                },
                "performance": {
                    "content": sections.get('performance', ''),
                    "priority": "high",
                    "dependencies": ["technical"],
                    "estimated_effort": "1-2 weeks"
                },
                "seo": {
                    "content": sections.get('seo', ''),
                    "priority": "medium",
                    "dependencies": ["content", "technical"],
                    "estimated_effort": "1-2 weeks"
                }
            },
            "implementation": {
                "roadmap": sections.get('implementation_roadmap', ''),
                "phases": self._define_implementation_phases(analysis_data),
                "team_requirements": self._recommend_team_composition(analysis_data),
                "timeline": self._create_project_timeline(analysis_data)
            },
            "quality_assurance": {
                "testing_strategy": self._define_testing_strategy(analysis_data),
                "performance_targets": self._set_performance_targets(analysis_data),
                "accessibility_requirements": self._define_accessibility_requirements(analysis_data),
                "deployment_checklist": self._create_deployment_checklist(analysis_data)
            }
        }
    
    def _format_as_markdown(self, sections: Dict[str, str], analysis_data: Dict[str, Any]) -> str:
        """Format prompt sections as enhanced Markdown documentation."""
        website_url = analysis_data.get('website_info', {}).get('url', 'analyzed website')
        website_type = analysis_data.get('website_info', {}).get('website_type', 'web application')
        
        return f"""# Website Recreation Guide
        
> **Source:** {website_url}  
> **Type:** {website_type.replace('_', ' ').title()}  
> **Generated:** {analysis_data.get('timestamp', 'Unknown')}

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Design Specifications](#design-specifications)
3. [Functionality Requirements](#functionality-requirements)
4. [Technical Implementation](#technical-implementation)
5. [Content Strategy](#content-strategy)
6. [User Experience](#user-experience)
7. [Accessibility](#accessibility)
8. [Performance](#performance)
9. [SEO Optimization](#seo-optimization)
10. [Implementation Roadmap](#implementation-roadmap)

---

## Executive Summary

{sections.get('executive_summary', '')}

---

## Design Specifications

{sections.get('design', '')}

---

## Functionality Requirements

{sections.get('functionality', '')}

---

## Technical Implementation

{sections.get('technical', '')}

---

## Content Strategy

{sections.get('content', '')}

---

## User Experience

{sections.get('user_experience', '')}

---

## Accessibility

{sections.get('accessibility', '')}

---

## Performance

{sections.get('performance', '')}

---

## SEO Optimization

{sections.get('seo', '')}

---

## Implementation Roadmap

{sections.get('implementation_roadmap', '')}

---

## Additional Resources

### Quality Checklist
- [ ] Design system implementation complete
- [ ] All functionality tested and validated
- [ ] Performance targets achieved
- [ ] Accessibility compliance verified
- [ ] SEO optimization implemented
- [ ] Content strategy executed
- [ ] User testing completed

### Tools & Technologies
- **Design:** Figma, Sketch, Adobe XD
- **Development:** Modern JavaScript frameworks, CSS preprocessors
- **Testing:** Jest, Cypress, Lighthouse, axe-core
- **Deployment:** CI/CD pipelines, cloud hosting
- **Monitoring:** Analytics, performance monitoring, error tracking

---

*This guide was generated using advanced AI analysis with multiple specialized models. Adapt recommendations based on your specific requirements and constraints.*
"""
    
    # Utility methods for enhanced functionality
    
    def _generate_executive_summary_enhanced(self, website_info: Dict[str, Any], business_model: Dict[str, Any]) -> str:
        """Generate enhanced executive summary using multi-modal AI."""
        try:
            prompt = f"""
            Generate a comprehensive executive summary for a web development project based on:
            
            Website Info: {website_info}
            Business Model: {business_model}
            
            Include project vision, scope, target audience, requirements summary, implementation strategy, and success metrics.
            """
            
            return self._generate_with_fallback(prompt, 'structured_output', use_multi_modal=True)
        except Exception:
            return self._fallback_executive_summary(website_info, business_model)
    
    def _generate_implementation_roadmap(self, analysis_data: Dict[str, Any], sections: Dict[str, str]) -> str:
        """Generate detailed implementation roadmap."""
        complexity = self._calculate_complexity_score(analysis_data)
        
        try:
            prompt = f"""
            Generate a detailed implementation roadmap for a web development project with complexity score {complexity}.
            
            Consider the following sections: {list(sections.keys())}
            
            Include phases, timelines, dependencies, team requirements, and risk mitigation strategies.
            """
            
            return self._generate_with_fallback(prompt, 'structured_output')
        except Exception:
            return """## Implementation Roadmap
            
**Phase 1: Foundation (Weeks 1-2)**
- Project setup and environment configuration
- Design system and component library creation
- Basic page structure and navigation

**Phase 2: Core Development (Weeks 3-6)**
- Main functionality implementation
- Content integration and management
- Responsive design implementation

**Phase 3: Enhancement (Weeks 7-8)**
- Performance optimization
- Accessibility improvements
- SEO implementation

**Phase 4: Testing & Launch (Weeks 9-10)**
- Comprehensive testing and bug fixes
- User acceptance testing
- Deployment and go-live"""
    
    def _calculate_complexity_score(self, analysis_data: Dict[str, Any]) -> int:
        """Calculate project complexity score (1-100)."""
        score = 50  # Base score
        
        # Add complexity based on features
        features = analysis_data.get('functionality_analysis', {}).get('core_features', [])
        score += len(features) * 5
        
        # Add complexity based on design sophistication
        design_system = analysis_data.get('design_analysis', {}).get('design_system', {})
        if design_system.get('systematic_approach') == 'methodical':
            score += 10
        
        # Add complexity based on technical requirements
        modern_features = analysis_data.get('technical_analysis', {}).get('modern_features', [])
        score += len(modern_features) * 3
        
        return min(score, 100)
    
    def _estimate_development_time(self, analysis_data: Dict[str, Any]) -> str:
        """Estimate development time based on complexity."""
        complexity = self._calculate_complexity_score(analysis_data)
        
        if complexity < 40:
            return "4-6 weeks"
        elif complexity < 70:
            return "6-10 weeks"
        else:
            return "10-16 weeks"
    
    def _recommend_team_size(self, analysis_data: Dict[str, Any]) -> str:
        """Recommend team size based on project complexity."""
        complexity = self._calculate_complexity_score(analysis_data)
        
        if complexity < 40:
            return "2-3 developers"
        elif complexity < 70:
            return "3-5 developers"
        else:
            return "5-8 developers"
    
    def _recommend_technologies(self, analysis_data: Dict[str, Any]) -> List[str]:
        """Recommend technologies based on analysis."""
        return [
            "React/Vue.js/Angular",
            "Node.js/Python/Java",
            "Modern CSS framework",
            "Database (SQL/NoSQL)",
            "Cloud hosting platform"
        ]
    
    # Placeholder methods for JSON formatting
    def _extract_key_objectives(self, analysis_data: Dict[str, Any]) -> List[str]:
        return ["User engagement", "Performance optimization", "Accessibility compliance"]
    
    def _define_success_criteria(self, analysis_data: Dict[str, Any]) -> List[str]:
        return ["Page load time <3s", "WCAG AA compliance", "95% user satisfaction"]
    
    def _identify_risk_factors(self, analysis_data: Dict[str, Any]) -> List[str]:
        return ["Technical complexity", "Timeline constraints", "Resource availability"]
    
    def _define_implementation_phases(self, analysis_data: Dict[str, Any]) -> List[Dict[str, str]]:
        return [
            {"phase": "Planning", "duration": "1-2 weeks", "deliverables": "Requirements and design"},
            {"phase": "Development", "duration": "6-8 weeks", "deliverables": "Core functionality"},
            {"phase": "Testing", "duration": "2-3 weeks", "deliverables": "Quality assurance"},
            {"phase": "Launch", "duration": "1 week", "deliverables": "Deployment and monitoring"}
        ]
    
    def _recommend_team_composition(self, analysis_data: Dict[str, Any]) -> Dict[str, str]:
        return {
            "frontend_developer": "1-2 developers",
            "backend_developer": "1-2 developers", 
            "ui_ux_designer": "1 designer",
            "project_manager": "1 PM",
            "qa_engineer": "1 tester"
        }
    
    def _create_project_timeline(self, analysis_data: Dict[str, Any]) -> Dict[str, str]:
        return {
            "total_duration": self._estimate_development_time(analysis_data),
            "start_to_mvp": "60% of total time",
            "testing_phase": "20% of total time",
            "deployment": "5% of total time"
        }
    
    def _define_testing_strategy(self, analysis_data: Dict[str, Any]) -> Dict[str, str]:
        return {
            "unit_testing": "Jest/Vitest framework",
            "integration_testing": "Cypress/Playwright",
            "accessibility_testing": "axe-core automated testing",
            "performance_testing": "Lighthouse CI integration"
        }
    
    def _set_performance_targets(self, analysis_data: Dict[str, Any]) -> Dict[str, str]:
        return {
            "page_load_time": "<3 seconds",
            "largest_contentful_paint": "<2.5 seconds",
            "first_input_delay": "<100 milliseconds",
            "cumulative_layout_shift": "<0.1"
        }
    
    def _define_accessibility_requirements(self, analysis_data: Dict[str, Any]) -> Dict[str, str]:
        return {
            "wcag_compliance": "AA level required",
            "keyboard_navigation": "Full support required",
            "screen_reader_support": "NVDA, JAWS, VoiceOver compatible",
            "color_contrast": "4.5:1 minimum ratio"
        }
    
    def _create_deployment_checklist(self, analysis_data: Dict[str, Any]) -> List[str]:
        return [
            "Performance optimization completed",
            "Accessibility testing passed",
            "Cross-browser testing completed",
            "Security audit completed",
            "SEO implementation verified",
            "Analytics and monitoring configured"
        ]