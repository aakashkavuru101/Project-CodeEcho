import React from 'react'
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
  Bot
} from 'lucide-react'

export default function LandingPage({ onGetStarted }) {
  const features = [
    {
      icon: <Bot className="h-12 w-12 text-blue-500" />,
      title: "4 AI Models",
      description: "Llama, Qwen, Mistral, and Gemma working together with automatic failover",
      highlight: "Multi-Model Intelligence"
    },
    {
      icon: <Shield className="h-12 w-12 text-green-500" />,
      title: "100% Private",
      description: "All processing happens locally with Ollama. Your data never leaves your environment.",
      highlight: "Zero Data Collection"
    },
    {
      icon: <Zap className="h-12 w-12 text-yellow-500" />,
      title: "Lightning Fast",
      description: "Optimized model selection for speed and accuracy. Get results in seconds.",
      highlight: "Sub-5 Second Analysis"
    },
    {
      icon: <Palette className="h-12 w-12 text-purple-500" />,
      title: "Design Intelligence",
      description: "Extract color palettes, typography, layouts, and visual hierarchy patterns.",
      highlight: "Design DNA Extraction"
    },
    {
      icon: <Code className="h-12 w-12 text-orange-500" />,
      title: "Technical Deep Dive",
      description: "Identify frameworks, libraries, performance patterns, and architecture decisions.",
      highlight: "Stack Detection"
    },
    {
      icon: <Users className="h-12 w-12 text-rose-500" />,
      title: "UX Analysis",
      description: "User journey mapping, conversion optimization, and accessibility insights.",
      highlight: "User Flow Mapping"
    }
  ];

  const stats = [
    { value: "4", label: "AI Models", sublabel: "Specialized for different tasks" },
    { value: "50+", label: "Analysis Points", sublabel: "Comprehensive coverage" },
    { value: "100%", label: "Privacy", sublabel: "Local processing only" },
    { value: "3", label: "Output Formats", sublabel: "Text, JSON, and Analysis" }
  ];

  const useCases = [
    {
      title: "Competitive Analysis",
      description: "Reverse engineer competitor websites to understand their design and technical choices",
      icon: <BarChart3 className="h-6 w-6 text-blue-500" />
    },
    {
      title: "Design Inspiration",
      description: "Extract design patterns and generate prompts to recreate similar aesthetics",
      icon: <Palette className="h-6 w-6 text-purple-500" />
    },
    {
      title: "Technical Learning",
      description: "Understand how modern websites are built and what technologies they use",
      icon: <Code className="h-6 w-6 text-orange-500" />
    },
    {
      title: "Client Proposals",
      description: "Generate detailed implementation guides for recreating website functionality",
      icon: <Users className="h-6 w-6 text-green-500" />
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/10" />
        <div className="container mx-auto px-4 py-16 md:py-24 relative">
          <div className="text-center max-w-4xl mx-auto">
            <div className="flex items-center justify-center mb-6">
              <div className="relative">
                <Globe className="h-16 w-16 md:h-20 md:w-20 text-blue-600" />
                <Sparkles className="h-6 w-6 text-yellow-500 absolute -top-2 -right-2 animate-pulse" />
              </div>
            </div>
            
            <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6">
              <span className="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                CodeEcho
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 mb-4">
              Reverse Engineer Any Website with AI
            </p>
            
            <p className="text-lg text-gray-500 mb-8 max-w-2xl mx-auto">
              Analyze websites and generate comprehensive prompts for recreating similar applications. 
              Powered by 4 specialized Ollama models running locally for complete privacy.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-3 sm:space-y-0 sm:space-x-4 mb-8">
              <Button 
                size="lg" 
                onClick={onGetStarted}
                className="px-8 py-3 text-lg bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                <Zap className="h-5 w-5 mr-2" />
                Try It Now - Free
                <ArrowRight className="h-5 w-5 ml-2" />
              </Button>
              
              <Button 
                size="lg" 
                variant="outline"
                className="px-8 py-3 text-lg border-2 hover:bg-gray-50"
                onClick={() => window.open('https://github.com', '_blank')}
              >
                <Github className="h-5 w-5 mr-2" />
                View on GitHub
              </Button>
            </div>
            
            <div className="flex flex-wrap items-center justify-center space-x-6 text-sm text-gray-500">
              <div className="flex items-center">
                <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                No API Keys Required
              </div>
              <div className="flex items-center">
                <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                100% Open Source
              </div>
              <div className="flex items-center">
                <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                Privacy First
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <Card key={index} className="text-center hover:shadow-lg transition-all duration-300 border-2 border-gray-100">
              <CardContent className="p-6">
                <div className="text-3xl md:text-4xl font-bold text-blue-600 mb-2">{stat.value}</div>
                <div className="font-semibold text-gray-900 mb-1">{stat.label}</div>
                <div className="text-sm text-gray-500">{stat.sublabel}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Features Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
            Powered by Advanced AI
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Four specialized AI models working together to provide the most comprehensive website analysis available
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="group hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 border-2 border-gray-100"
            >
              <CardContent className="p-8">
                <div className="flex items-center justify-between mb-6">
                  <div className="p-3 rounded-xl bg-gray-50 group-hover:bg-white transition-colors">
                    {feature.icon}
                  </div>
                  <Badge variant="secondary" className="text-xs font-medium">
                    {feature.highlight}
                  </Badge>
                </div>
                <h3 className="text-xl font-bold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>

      {/* Use Cases Section */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Perfect For Every Use Case
            </h2>
            <p className="text-xl text-gray-600">
              Whether you're a developer, designer, or entrepreneur, CodeEcho adapts to your needs
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {useCases.map((useCase, index) => (
              <Card key={index} className="hover:shadow-lg transition-all duration-300 border border-white/50 bg-white/70 backdrop-blur-sm">
                <CardContent className="p-6">
                  <div className="flex items-start space-x-4">
                    <div className="p-2 rounded-lg bg-white">
                      {useCase.icon}
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900 mb-2">{useCase.title}</h3>
                      <p className="text-gray-600">{useCase.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-4 py-16">
        <Card className="border-2 border-blue-200 bg-gradient-to-r from-blue-50 to-purple-50">
          <CardContent className="p-12 text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Ready to Reverse Engineer?
            </h2>
            <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
              Start analyzing websites with AI-powered precision. No signup required, completely free and private.
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-3 sm:space-y-0 sm:space-x-4">
              <Button 
                size="lg" 
                onClick={onGetStarted}
                className="px-8 py-3 text-lg bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700"
              >
                <Sparkles className="h-5 w-5 mr-2" />
                Get Started Now
              </Button>
              
              <Button 
                size="lg" 
                variant="outline"
                className="px-8 py-3 text-lg border-2"
                onClick={() => window.open('https://ollama.ai', '_blank')}
              >
                <ExternalLink className="h-5 w-5 mr-2" />
                Learn About Ollama
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="flex items-center justify-center mb-4">
              <Globe className="h-8 w-8 text-blue-400 mr-2" />
              <span className="text-xl font-bold">CodeEcho</span>
            </div>
            <p className="text-gray-400 mb-4">
              AI-powered website reverse engineering for developers and designers
            </p>
            <div className="flex items-center justify-center space-x-6 text-gray-400">
              <span>Powered by Ollama</span>
              <span>•</span>
              <span>Open Source</span>
              <span>•</span>
              <span>Privacy First</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}