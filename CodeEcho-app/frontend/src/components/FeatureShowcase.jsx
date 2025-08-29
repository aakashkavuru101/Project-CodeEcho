import React from 'react'
import { Card, CardContent } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Globe, 
  Zap, 
  Shield, 
  Palette, 
  Code, 
  Users,
  TrendingUp,
  CheckCircle
} from 'lucide-react'

export default function FeatureShowcase() {
  const features = [
    {
      icon: <Zap className="h-8 w-8 text-yellow-500" />,
      title: "AI-Powered Analysis",
      description: "Advanced analysis using 4 specialized Ollama models",
      badge: "Fast",
      color: "bg-yellow-50 border-yellow-200"
    },
    {
      icon: <Shield className="h-8 w-8 text-green-500" />,
      title: "Secure & Private",
      description: "Local AI processing, no data leaves your environment",
      badge: "Secure",
      color: "bg-green-50 border-green-200"
    },
    {
      icon: <Palette className="h-8 w-8 text-purple-500" />,
      title: "Design Intelligence",
      description: "Extract design patterns, colors, and typography",
      badge: "Creative",
      color: "bg-purple-50 border-purple-200"
    },
    {
      icon: <Code className="h-8 w-8 text-blue-500" />,
      title: "Technical Analysis",
      description: "Identify frameworks, performance metrics, and tech stack",
      badge: "Technical",
      color: "bg-blue-50 border-blue-200"
    },
    {
      icon: <Users className="h-8 w-8 text-rose-500" />,
      title: "UX Insights",
      description: "User experience patterns and interaction analysis",
      badge: "User-Focused",
      color: "bg-rose-50 border-rose-200"
    },
    {
      icon: <TrendingUp className="h-8 w-8 text-emerald-500" />,
      title: "Business Model",
      description: "Revenue strategies and value proposition analysis",
      badge: "Strategic",
      color: "bg-emerald-50 border-emerald-200"
    }
  ];

  const stats = [
    { label: "AI Models", value: "8", icon: <Globe className="h-4 w-4" /> },
    { label: "Analysis Points", value: "50+", icon: <CheckCircle className="h-4 w-4" /> },
    { label: "Output Formats", value: "3", icon: <Code className="h-4 w-4" /> },
    { label: "Fallback Systems", value: "100%", icon: <Shield className="h-4 w-4" /> }
  ];

  return (
    <div className="w-full space-y-8">
      {/* Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map((stat, index) => (
          <Card key={index} className="text-center p-4">
            <CardContent className="p-0">
              <div className="flex items-center justify-center mb-2 text-blue-600">
                {stat.icon}
              </div>
              <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Feature Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {features.map((feature, index) => (
          <Card 
            key={index} 
            className={`${feature.color} border-2 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1`}
          >
            <CardContent className="p-6">
              <div className="flex items-start justify-between mb-4">
                <div className="p-2 rounded-lg bg-white/70">
                  {feature.icon}
                </div>
                <Badge variant="secondary" className="text-xs">
                  {feature.badge}
                </Badge>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">{feature.title}</h3>
              <p className="text-sm text-gray-600">{feature.description}</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Model Performance Indicators */}
      <Card className="border-2 border-blue-200 bg-blue-50/50">
        <CardContent className="p-6">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center">
            <Zap className="h-5 w-5 mr-2 text-blue-600" />
            AI Model Performance
          </h3>
          <div className="space-y-4">
            {[
              { name: "Llama 3.1 8B", type: "Primary", accuracy: 95, speed: 90 },
              { name: "Qwen 2.5 7B", type: "Reasoning", accuracy: 92, speed: 85 },
              { name: "Mistral 7B", type: "Creative", accuracy: 88, speed: 95 },
              { name: "Gemma 2 9B", type: "Detailed", accuracy: 94, speed: 80 }
            ].map((model, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className="font-medium text-sm">{model.name}</span>
                    <Badge variant="outline" className="text-xs">{model.type}</Badge>
                  </div>
                  <div className="text-xs text-gray-600">
                    Accuracy: {model.accuracy}% | Speed: {model.speed}%
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Accuracy</div>
                    <Progress value={model.accuracy} className="h-2" />
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">Speed</div>
                    <Progress value={model.speed} className="h-2" />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}