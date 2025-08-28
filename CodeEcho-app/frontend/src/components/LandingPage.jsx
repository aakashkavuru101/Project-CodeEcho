import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Globe, 
  Zap, 
  Shield, 
  Code, 
  Palette, 
  Users,
  CheckCircle,
  ArrowRight,
  Github,
  ExternalLink,
  Sparkles,
  BarChart3,
  Bot,
  Star,
  Cpu,
  Target,
  Layers,
  Lightbulb,
  Rocket,
  Heart,
  TrendingUp,
  Award,
  Zap as Lightning
} from 'lucide-react'

export default function LandingPage({ onGetStarted }) {
  const [animationIndex, setAnimationIndex] = useState(0)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    setIsVisible(true)
    const interval = setInterval(() => {
      setAnimationIndex(prev => (prev + 1) % 4)
    }, 2000)
    return () => clearInterval(interval)
  }, [])

  const enhancedFeatures = [
    {
      icon: <Bot className="h-12 w-12 text-blue-500" />,
      title: "8 Specialized AI Models",
      description: "Llama, Qwen, Mistral, Gemma, Phi3, CodeLlama, Neural-Chat, and Vicuna working together with intelligent routing",
      highlight: "Multi-Modal Intelligence",
      color: "blue",
      details: ["Smart model selection", "Automatic failover", "Performance optimization", "Task specialization"]
    },
    {
      icon: <Shield className="h-12 w-12 text-green-500" />,
      title: "100% Private & Secure",
      description: "All processing happens locally with Ollama. Your data never leaves your environment. Zero tracking, zero data collection.",
      highlight: "Privacy First",
      color: "green",
      details: ["Local processing", "No data collection", "GDPR compliant", "Open source"]
    },
    {
      icon: <Lightning className="h-12 w-12 text-yellow-500" />,
      title: "Lightning Fast Analysis",
      description: "Optimized model selection and caching for speed. Get comprehensive analysis results in under 10 seconds.",
      highlight: "Sub-10 Second Results",
      color: "yellow",
      details: ["Smart caching", "Parallel processing", "Optimized prompts", "Real-time feedback"]
    },
    {
      icon: <Palette className="h-12 w-12 text-purple-500" />,
      title: "Advanced Design Intelligence",
      description: "Extract color psychology, typography pairing, visual hierarchy, design systems, and modern patterns.",
      highlight: "Design DNA Analysis",
      color: "purple",
      details: ["Color psychology", "Typography analysis", "Design patterns", "Brand recognition"]
    },
    {
      icon: <Code className="h-12 w-12 text-orange-500" />,
      title: "Deep Technical Analysis",
      description: "Identify frameworks, architecture patterns, performance optimizations, security measures, and deployment strategies.",
      highlight: "Full Stack Detection",
      color: "orange",
      details: ["Framework detection", "Performance analysis", "Security audit", "Architecture review"]
    },
    {
      icon: <Users className="h-12 w-12 text-rose-500" />,
      title: "Comprehensive UX Analysis",
      description: "User journey mapping, conversion optimization, accessibility insights, and interaction pattern analysis.",
      highlight: "UX Intelligence",
      color: "rose",
      details: ["User flow mapping", "Conversion analysis", "Accessibility audit", "Interaction patterns"]
    }
  ];

  const enhancedStats = [
    { value: "8", label: "AI Models", sublabel: "Specialized for different tasks", icon: <Bot className="h-6 w-6" /> },
    { value: "100+", label: "Analysis Points", sublabel: "Comprehensive coverage", icon: <Target className="h-6 w-6" /> },
    { value: "100%", label: "Privacy", sublabel: "Local processing only", icon: <Shield className="h-6 w-6" /> },
    { value: "5", label: "Output Formats", sublabel: "Text, JSON, Markdown & more", icon: <Layers className="h-6 w-6" /> }
  ];

  const enhancedUseCases = [
    {
      title: "Competitive Intelligence",
      description: "Deep-dive into competitor websites to understand their design philosophy, technical choices, and UX strategies",
      icon: <BarChart3 className="h-6 w-6 text-blue-500" />,
      benefits: ["Strategic insights", "Market analysis", "Technology trends", "Design patterns"]
    },
    {
      title: "Design System Creation",
      description: "Extract comprehensive design tokens, component patterns, and style guides to build your own design system",
      icon: <Palette className="h-6 w-6 text-purple-500" />,
      benefits: ["Design tokens", "Component library", "Style guide", "Brand consistency"]
    },
    {
      title: "Technical Architecture",
      description: "Understand modern web architecture, performance optimizations, and best practices from real-world applications",
      icon: <Code className="h-6 w-6 text-orange-500" />,
      benefits: ["Architecture patterns", "Performance insights", "Best practices", "Technology stack"]
    },
    {
      title: "Client Proposals & Specs",
      description: "Generate detailed technical specifications and implementation guides for client projects and proposals",
      icon: <Users className="h-6 w-6 text-green-500" />,
      benefits: ["Technical specs", "Project estimates", "Implementation guide", "Client communication"]
    }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "Senior Developer",
      content: "CodeEcho has revolutionized how I analyze competitor sites. The AI insights are incredibly detailed.",
      rating: 5
    },
    {
      name: "Michael Rodriguez",
      role: "UX Designer",
      content: "The design analysis is spot-on. It captures nuances I would miss and presents them clearly.",
      rating: 5
    },
    {
      name: "Emily Watson",
      role: "Product Manager",
      content: "Perfect for creating detailed technical specs. Saves me hours of manual analysis work.",
      rating: 5
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-blue-900 dark:to-purple-900">
      {/* Enhanced Hero Section with Animation */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10" />
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-4 -left-4 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob"></div>
          <div className="absolute -top-4 -right-4 w-72 h-72 bg-yellow-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-2000"></div>
          <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-blob animation-delay-4000"></div>
        </div>
        
        <div className={`container mx-auto px-4 py-16 md:py-24 relative transition-all duration-1000 ${isVisible ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
          <div className="text-center max-w-5xl mx-auto">
            <div className="flex items-center justify-center mb-8">
              <div className="relative group">
                <div className="absolute -inset-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-lg opacity-25 group-hover:opacity-40 transition duration-1000"></div>
                <Globe className="h-20 w-20 md:h-24 md:w-24 text-blue-600 relative animate-pulse" />
                <Sparkles className="h-8 w-8 text-yellow-500 absolute -top-3 -right-3 animate-bounce" />
                <div className="absolute -bottom-2 -left-2 p-2 bg-white rounded-full shadow-lg">
                  <Bot className="h-4 w-4 text-blue-600 animate-pulse" />
                </div>
              </div>
            </div>
            
            <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold text-gray-900 dark:text-white mb-8 leading-tight">
              <span className="bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent bg-300% animate-gradient">
                CodeEcho
              </span>
              <div className="text-2xl md:text-3xl lg:text-4xl mt-4 font-normal text-gray-600 dark:text-gray-300">
                AI-Powered Website Reverse Engineering
              </div>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-6 font-medium">
              Transform any website into detailed implementation blueprints
            </p>
            
            <p className="text-lg text-gray-500 dark:text-gray-400 mb-10 max-w-3xl mx-auto leading-relaxed">
              Analyze websites with 8 specialized AI models and generate comprehensive technical specifications, 
              design systems, and implementation guides. All processing happens locally for complete privacy.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-12">
              <Button 
                size="lg" 
                onClick={onGetStarted}
                className="group px-10 py-4 text-lg font-semibold bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-xl"
              >
                <Rocket className="h-6 w-6 mr-3 group-hover:animate-bounce" />
                Start Analyzing Now
                <ArrowRight className="h-6 w-6 ml-3 group-hover:translate-x-1 transition-transform" />
              </Button>
              
              <Button 
                size="lg" 
                variant="outline"
                className="px-10 py-4 text-lg font-semibold border-2 border-gray-300 hover:border-gray-400 hover:bg-gray-50 dark:hover:bg-gray-800 transition-all duration-200"
                onClick={() => window.open('https://github.com/aakashkavuru101/Project-CodeEcho', '_blank')}
              >
                <Github className="h-6 w-6 mr-3" />
                View Source Code
                <ExternalLink className="h-4 w-4 ml-2" />
              </Button>
            </div>
            
            <div className="flex flex-wrap items-center justify-center gap-6 text-sm text-gray-500 dark:text-gray-400">
              <div className="flex items-center bg-white/50 dark:bg-gray-800/50 px-4 py-2 rounded-full backdrop-blur-sm">
                <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                No API Keys Required
              </div>
              <div className="flex items-center bg-white/50 dark:bg-gray-800/50 px-4 py-2 rounded-full backdrop-blur-sm">
                <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                100% Open Source
              </div>
              <div className="flex items-center bg-white/50 dark:bg-gray-800/50 px-4 py-2 rounded-full backdrop-blur-sm">
                <CheckCircle className="h-5 w-5 text-green-500 mr-2" />
                Privacy First Design
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Enhanced Stats Section with Animation */}
      <div className="container mx-auto px-4 py-20">
        <div className="text-center mb-12">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Powered by Advanced AI Technology
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            Industry-leading analysis capabilities with local processing
          </p>
        </div>
        
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          {enhancedStats.map((stat, index) => (
            <Card key={index} className="group text-center hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 border-2 border-gray-100 dark:border-gray-700 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
              <CardContent className="p-8">
                <div className="flex items-center justify-center mb-4">
                  <div className="p-3 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 text-white group-hover:scale-110 transition-transform duration-300">
                    {stat.icon}
                  </div>
                </div>
                <div className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">
                  {stat.value}
                </div>
                <div className="font-semibold text-gray-900 dark:text-white mb-2 text-lg">{stat.label}</div>
                <div className="text-sm text-gray-500 dark:text-gray-400">{stat.sublabel}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Enhanced Features Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <Badge className="mb-4 px-4 py-2 text-sm font-medium bg-gradient-to-r from-blue-500 to-purple-600 text-white">
            ✨ Advanced AI Capabilities
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            8 Specialized AI Models
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 max-w-4xl mx-auto leading-relaxed">
            Each model is optimized for specific analysis tasks, working together to provide 
            the most comprehensive website reverse engineering available anywhere.
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
          {enhancedFeatures.map((feature, index) => (
            <Card 
              key={index} 
              className="group hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-3 border-2 border-gray-100 dark:border-gray-700 overflow-hidden bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm"
            >
              <CardContent className="p-8 relative">
                <div className={`absolute top-0 left-0 w-2 h-full bg-gradient-to-b from-${feature.color}-400 to-${feature.color}-600`}></div>
                
                <div className="flex items-center justify-between mb-6">
                  <div className="p-4 rounded-xl bg-gray-50 dark:bg-gray-700 group-hover:bg-white dark:group-hover:bg-gray-600 transition-all duration-300 group-hover:scale-110">
                    {feature.icon}
                  </div>
                  <Badge variant="secondary" className="text-xs font-medium px-3 py-1 bg-gradient-to-r from-gray-100 to-gray-200 dark:from-gray-700 dark:to-gray-600">
                    {feature.highlight}
                  </Badge>
                </div>
                
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 group-hover:text-blue-600 transition-colors">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 leading-relaxed mb-6">
                  {feature.description}
                </p>
                
                <div className="space-y-2">
                  {feature.details.map((detail, idx) => (
                    <div key={idx} className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                      <CheckCircle className="h-4 w-4 text-green-500 mr-2 flex-shrink-0" />
                      {detail}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Enhanced Use Cases Section */}
      <div className="bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 dark:from-gray-800 dark:via-blue-900 dark:to-purple-900 py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <Badge className="mb-4 px-4 py-2 text-sm font-medium bg-gradient-to-r from-purple-500 to-pink-600 text-white">
              🎯 Real-World Applications
            </Badge>
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
              Perfect For Every Professional
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              Whether you're a developer, designer, product manager, or entrepreneur, 
              CodeEcho provides the insights you need to build better products.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {enhancedUseCases.map((useCase, index) => (
              <Card key={index} className="group hover:shadow-xl transition-all duration-500 transform hover:-translate-y-2 border border-white/50 bg-white/80 dark:bg-gray-800/80 backdrop-blur-lg">
                <CardContent className="p-8">
                  <div className="flex items-start space-x-6">
                    <div className="p-4 rounded-xl bg-white dark:bg-gray-700 shadow-lg group-hover:scale-110 transition-transform duration-300">
                      {useCase.icon}
                    </div>
                    <div className="flex-1">
                      <h3 className="font-bold text-xl text-gray-900 dark:text-white mb-3 group-hover:text-blue-600 transition-colors">
                        {useCase.title}
                      </h3>
                      <p className="text-gray-600 dark:text-gray-300 mb-4 leading-relaxed">
                        {useCase.description}
                      </p>
                      <div className="grid grid-cols-2 gap-2">
                        {useCase.benefits.map((benefit, idx) => (
                          <div key={idx} className="flex items-center text-sm text-gray-500 dark:text-gray-400">
                            <Star className="h-3 w-3 text-yellow-500 mr-2 flex-shrink-0" />
                            {benefit}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* New Testimonials Section */}
      <div className="container mx-auto px-4 py-20">
        <div className="text-center mb-16">
          <Badge className="mb-4 px-4 py-2 text-sm font-medium bg-gradient-to-r from-green-500 to-blue-600 text-white">
            💬 User Testimonials
          </Badge>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
            Loved by Professionals
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300">
            See what developers and designers are saying about CodeEcho
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <Card key={index} className="hover:shadow-lg transition-all duration-300 bg-white/70 dark:bg-gray-800/70 backdrop-blur-sm">
              <CardContent className="p-6">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="h-5 w-5 text-yellow-500 fill-current" />
                  ))}
                </div>
                <p className="text-gray-600 dark:text-gray-300 mb-4 italic">
                  "{testimonial.content}"
                </p>
                <div className="flex items-center">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold mr-3">
                    {testimonial.name.charAt(0)}
                  </div>
                  <div>
                    <div className="font-semibold text-gray-900 dark:text-white">{testimonial.name}</div>
                    <div className="text-sm text-gray-500 dark:text-gray-400">{testimonial.role}</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Enhanced CTA Section */}
      <div className="container mx-auto px-4 py-20">
        <Card className="border-4 border-blue-200 dark:border-blue-700 bg-gradient-to-r from-blue-50 via-purple-50 to-pink-50 dark:from-gray-800 dark:via-blue-900 dark:to-purple-900 overflow-hidden relative">
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/5 to-purple-600/5"></div>
          <CardContent className="p-16 text-center relative">
            <div className="max-w-4xl mx-auto">
              <div className="flex items-center justify-center mb-8">
                <div className="p-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full">
                  <Rocket className="h-12 w-12 text-white" />
                </div>
              </div>
              
              <h2 className="text-4xl md:text-5xl font-bold text-gray-900 dark:text-white mb-6">
                Ready to Revolutionize Your Analysis?
              </h2>
              <p className="text-xl text-gray-600 dark:text-gray-300 mb-10 max-w-3xl mx-auto leading-relaxed">
                Join thousands of developers and designers who use CodeEcho to understand, 
                learn from, and recreate amazing websites. Start your analysis in seconds.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6">
                <Button 
                  size="lg" 
                  onClick={onGetStarted}
                  className="group px-12 py-4 text-xl font-semibold bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transform hover:scale-105 transition-all duration-200 shadow-lg hover:shadow-2xl"
                >
                  <Lightning className="h-6 w-6 mr-3 group-hover:animate-pulse" />
                  Start Free Analysis
                  <Heart className="h-6 w-6 ml-3 text-red-400 group-hover:animate-pulse" />
                </Button>
                
                <div className="text-sm text-gray-500 dark:text-gray-400 italic">
                  No signup • No credit card • 100% free
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}