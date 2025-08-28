import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Globe, 
  Download, 
  Loader2, 
  CheckCircle, 
  AlertCircle, 
  Code, 
  Palette, 
  Settings, 
  Users, 
  FileText,
  Zap
} from 'lucide-react'
import config from './config.js'
import './App.css'

function App() {
  const [url, setUrl] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState(null)
  const [sessionId, setSessionId] = useState(null)
  const [progress, setProgress] = useState(0)

  const analyzeWebsite = async () => {
    if (!url.trim()) {
      setError('Please enter a valid URL')
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setProgress(0)
    
    try {
      // Simulate progress updates
      const progressInterval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval)
            return 90
          }
          return prev + 10
        })
      }, 500)

      const response = await fetch(`${config.API_BASE_URL}/api/analyze-website`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: url.trim() }),
      })

      const data = await response.json()
      
      clearInterval(progressInterval)
      setProgress(100)

      if (data.status === 'success') {
        setAnalysisResult(data)
        setSessionId(data.session_id)
      } else {
        setError(data.message || 'Analysis failed')
      }
    } catch (err) {
      setError('Failed to connect to the analysis service')
      console.error('Analysis error:', err)
    } finally {
      setIsAnalyzing(false)
    }
  }

  const downloadResults = async () => {
    if (!sessionId) return
    
    try {
      const response = await fetch(`${config.API_BASE_URL}/api/download/${sessionId}`)
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url
        a.download = `website_analysis_${sessionId.slice(0, 8)}.zip`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        setError('Failed to download results')
      }
    } catch (err) {
      setError('Download failed')
      console.error('Download error:', err)
    }
  }

  const resetAnalysis = () => {
    setAnalysisResult(null)
    setSessionId(null)
    setError(null)
    setProgress(0)
    setUrl('')
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center mb-4">
            <Globe className="h-12 w-12 text-blue-600 mr-3" />
            <h1 className="text-4xl font-bold text-gray-900">Website Reverse Engineer</h1>
          </div>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            AI-powered tool to analyze any website and generate comprehensive prompts for recreating similar applications
          </p>
        </div>

        {/* Main Content */}
        {!analysisResult ? (
          <div className="max-w-2xl mx-auto">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="h-5 w-5 mr-2 text-blue-600" />
                  Analyze Website
                </CardTitle>
                <CardDescription>
                  Enter a website URL to extract its design patterns, functionality, and generate AI prompts for recreation
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex space-x-2">
                  <Input
                    type="url"
                    placeholder="https://example.com"
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    disabled={isAnalyzing}
                    className="flex-1"
                  />
                  <Button 
                    onClick={analyzeWebsite} 
                    disabled={isAnalyzing || !url.trim()}
                    className="px-6"
                  >
                    {isAnalyzing ? (
                      <>
                        <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                        Analyzing...
                      </>
                    ) : (
                      'Analyze'
                    )}
                  </Button>
                </div>

                {isAnalyzing && (
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm text-gray-600">
                      <span>Analysis Progress</span>
                      <span>{progress}%</span>
                    </div>
                    <Progress value={progress} className="w-full" />
                    <p className="text-sm text-gray-500 text-center">
                      {progress < 30 ? 'Scraping website content...' :
                       progress < 60 ? 'Analyzing design and functionality...' :
                       progress < 90 ? 'Generating AI prompts...' :
                       'Finalizing results...'}
                    </p>
                  </div>
                )}

                {error && (
                  <Alert variant="destructive">
                    <AlertCircle className="h-4 w-4" />
                    <AlertDescription>{error}</AlertDescription>
                  </Alert>
                )}

                <div className="bg-blue-50 p-4 rounded-lg">
                  <h3 className="font-semibold text-blue-900 mb-2">What you'll get:</h3>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• Comprehensive design analysis (colors, typography, layout)</li>
                    <li>• Functionality breakdown (features, interactions, user flows)</li>
                    <li>• Technical implementation recommendations</li>
                    <li>• Content strategy and UX guidelines</li>
                    <li>• Ready-to-use AI prompts in text and JSON formats</li>
                  </ul>
                </div>
              </CardContent>
            </Card>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Success Header */}
            <div className="text-center">
              <CheckCircle className="h-16 w-16 text-green-600 mx-auto mb-4" />
              <h2 className="text-3xl font-bold text-gray-900 mb-2">Analysis Complete!</h2>
              <p className="text-gray-600">
                Successfully analyzed <span className="font-semibold">{analysisResult.analysis.website_info.url}</span>
              </p>
            </div>

            {/* Quick Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4 text-center">
                  <Globe className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">Website Type</p>
                  <p className="font-semibold capitalize">
                    {analysisResult.analysis.summary.website_type.replace('_', ' ')}
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 text-center">
                  <Users className="h-8 w-8 text-green-600 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">Primary Purpose</p>
                  <p className="font-semibold capitalize">
                    {analysisResult.analysis.summary.primary_purpose}
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 text-center">
                  <Settings className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">Core Features</p>
                  <p className="font-semibold">
                    {analysisResult.analysis.summary.core_features.length} identified
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardContent className="p-4 text-center">
                  <Code className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                  <p className="text-sm text-gray-600">Business Type</p>
                  <p className="font-semibold capitalize">
                    {analysisResult.analysis.summary.business_type.replace('_', ' ')}
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Analysis Results */}
            <Card>
              <CardHeader>
                <CardTitle>Analysis Results</CardTitle>
                <CardDescription>
                  Detailed breakdown of the website's design, functionality, and technical implementation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="overview" className="w-full">
                  <TabsList className="grid w-full grid-cols-5">
                    <TabsTrigger value="overview">Overview</TabsTrigger>
                    <TabsTrigger value="design">Design</TabsTrigger>
                    <TabsTrigger value="functionality">Features</TabsTrigger>
                    <TabsTrigger value="technical">Technical</TabsTrigger>
                    <TabsTrigger value="prompts">Prompts</TabsTrigger>
                  </TabsList>

                  <TabsContent value="overview" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2">Website Information</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Type:</span>
                            <Badge variant="secondary">
                              {analysisResult.analysis.website_info.website_type}
                            </Badge>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Purpose:</span>
                            <span>{analysisResult.analysis.website_info.primary_purpose}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Industry:</span>
                            <span>{analysisResult.analysis.website_info.industry_category}</span>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Core Features</h4>
                        <div className="flex flex-wrap gap-1">
                          {analysisResult.analysis.summary.core_features.map((feature, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {feature.replace('_', ' ')}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="design" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2 flex items-center">
                          <Palette className="h-4 w-4 mr-2" />
                          Color Palette
                        </h4>
                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="text-gray-600">Scheme: </span>
                            <Badge variant="secondary">
                              {analysisResult.analysis.design_analysis.color_palette?.color_scheme || 'Unknown'}
                            </Badge>
                          </div>
                          <div>
                            <span className="text-gray-600">Mood: </span>
                            <span>{analysisResult.analysis.design_analysis.color_palette?.mood || 'Unknown'}</span>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Typography</h4>
                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="text-gray-600">Type: </span>
                            <Badge variant="outline">
                              {analysisResult.analysis.design_analysis.typography?.font_type || 'Unknown'}
                            </Badge>
                          </div>
                          <div>
                            <span className="text-gray-600">Strategy: </span>
                            <span>{analysisResult.analysis.design_analysis.typography?.typography_strategy || 'Unknown'}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="functionality" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2">User Interactions</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Buttons:</span>
                            <span>{analysisResult.analysis.functionality_analysis.user_interactions?.button_count || 0}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Links:</span>
                            <span>{analysisResult.analysis.functionality_analysis.user_interactions?.link_count || 0}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Inputs:</span>
                            <span>{analysisResult.analysis.functionality_analysis.user_interactions?.input_count || 0}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Complexity:</span>
                            <Badge variant="outline">
                              {analysisResult.analysis.functionality_analysis.user_interactions?.interaction_complexity || 'Unknown'}
                            </Badge>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Navigation</h4>
                        <div className="space-y-2 text-sm">
                          <div className="flex justify-between">
                            <span className="text-gray-600">Items:</span>
                            <span>{analysisResult.analysis.functionality_analysis.navigation_structure?.navigation_items || 0}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Search:</span>
                            <Badge variant={analysisResult.analysis.functionality_analysis.navigation_structure?.has_search ? "default" : "secondary"}>
                              {analysisResult.analysis.functionality_analysis.navigation_structure?.has_search ? "Yes" : "No"}
                            </Badge>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-gray-600">Pattern:</span>
                            <span>{analysisResult.analysis.functionality_analysis.navigation_structure?.navigation_pattern || 'Unknown'}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="technical" className="space-y-4">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <h4 className="font-semibold mb-2">Technologies</h4>
                        <div className="flex flex-wrap gap-1">
                          {analysisResult.analysis.technical_analysis.frontend_technologies?.map((tech, index) => (
                            <Badge key={index} variant="outline">
                              {tech}
                            </Badge>
                          )) || <span className="text-gray-500">None detected</span>}
                        </div>
                      </div>
                      <div>
                        <h4 className="font-semibold mb-2">Modern Features</h4>
                        <div className="flex flex-wrap gap-1">
                          {analysisResult.analysis.technical_analysis.modern_features?.map((feature, index) => (
                            <Badge key={index} variant="secondary">
                              {feature.replace('_', ' ')}
                            </Badge>
                          )) || <span className="text-gray-500">None detected</span>}
                        </div>
                      </div>
                    </div>
                  </TabsContent>

                  <TabsContent value="prompts" className="space-y-4">
                    <div className="bg-gray-50 p-4 rounded-lg">
                      <h4 className="font-semibold mb-2 flex items-center">
                        <FileText className="h-4 w-4 mr-2" />
                        Generated Prompt Preview
                      </h4>
                      <div className="bg-white p-3 rounded border text-sm font-mono max-h-64 overflow-y-auto">
                        {analysisResult.prompts.text_preview}
                      </div>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <h5 className="font-semibold mb-2">Prompt Sections</h5>
                        <div className="space-y-1">
                          <div className="flex justify-between">
                            <span>Design:</span>
                            <span>{analysisResult.prompts.json_preview.requirements_summary?.design || 0} chars</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Functionality:</span>
                            <span>{analysisResult.prompts.json_preview.requirements_summary?.functionality || 0} chars</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Technical:</span>
                            <span>{analysisResult.prompts.json_preview.requirements_summary?.technical || 0} chars</span>
                          </div>
                          <div className="flex justify-between">
                            <span>Content:</span>
                            <span>{analysisResult.prompts.json_preview.requirements_summary?.content || 0} chars</span>
                          </div>
                          <div className="flex justify-between">
                            <span>UX:</span>
                            <span>{analysisResult.prompts.json_preview.requirements_summary?.user_experience || 0} chars</span>
                          </div>
                        </div>
                      </div>
                      <div>
                        <h5 className="font-semibold mb-2">Output Formats</h5>
                        <div className="space-y-1">
                          <div className="flex items-center">
                            <FileText className="h-4 w-4 mr-2 text-blue-600" />
                            <span>Human-readable text prompt</span>
                          </div>
                          <div className="flex items-center">
                            <Code className="h-4 w-4 mr-2 text-green-600" />
                            <span>Structured JSON format</span>
                          </div>
                          <div className="flex items-center">
                            <Settings className="h-4 w-4 mr-2 text-purple-600" />
                            <span>Complete analysis data</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>

            {/* Action Buttons */}
            <div className="flex justify-center space-x-4">
              <Button onClick={downloadResults} size="lg" className="px-8">
                <Download className="h-4 w-4 mr-2" />
                Download Results
              </Button>
              <Button onClick={resetAnalysis} variant="outline" size="lg" className="px-8">
                Analyze Another Website
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

