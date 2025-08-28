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
  Zap,
  Sparkles,
  BarChart3,
  History
} from 'lucide-react'
import config from './config.js'
import FeatureShowcase from './components/FeatureShowcase.jsx'
import AnalysisHistory from './components/AnalysisHistory.jsx'
import LiveDashboard from './components/LiveDashboard.jsx'
import LandingPage from './components/LandingPage.jsx'
import Header from './components/Header.jsx'
import { ThemeProvider, useTheme, useLanguage } from './contexts/ThemeContext.jsx'
import { useTranslation } from './utils/translations.js'
import './App.css'

function AppContent() {
  const { language } = useLanguage()
  const t = useTranslation(language)
  const [url, setUrl] = useState('')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState(null)
  const [sessionId, setSessionId] = useState(null)
  const [progress, setProgress] = useState(0)
  const [currentView, setCurrentView] = useState('landing') // 'landing', 'analyze', 'dashboard', 'history'

  const analyzeWebsite = async (websiteUrl = null) => {
    const targetUrl = websiteUrl || url;
    if (!targetUrl.trim()) {
      setError(t('errorUrlRequired'))
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setProgress(0)
    setCurrentView('analyze')
    
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
        body: JSON.stringify({ url: targetUrl.trim() }),
      })

      const data = await response.json()
      
      clearInterval(progressInterval)
      setProgress(100)

      if (data.status === 'success') {
        setAnalysisResult(data)
        setSessionId(data.session_id)
      } else {
        setError(data.message || t('errorAnalysisFailed'))
      }
    } catch (err) {
      setError(t('errorConnection'))
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
    setCurrentView('analyze')
  }

  const handleGetStarted = () => {
    setCurrentView('analyze')
  }

  // Show landing page first
  if (currentView === 'landing') {
    return <LandingPage onGetStarted={handleGetStarted} />
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-6 md:py-8">
        {/* Enhanced Header */}
        <div className="text-center mb-8 md:mb-12">
          <div className="flex items-center justify-center mb-4">
            <div className="relative">
              <Globe className="h-10 w-10 md:h-12 md:w-12 text-blue-600 mr-3" />
              <Sparkles className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1 animate-pulse" />
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-foreground">{t('title')}</h1>
          </div>
          <div className="max-w-3xl mx-auto space-y-2">
            <p className="text-lg md:text-xl text-muted-foreground">
              {t('subtitle')}
            </p>
            <p className="text-sm md:text-base text-muted-foreground">
              {t('secureSubtitle')}
            </p>
          </div>
          
          {/* Navigation Tabs */}
          <div className="mt-6">
            <div className="flex justify-center">
              <div className="inline-flex rounded-lg border bg-white p-1">
                <Button
                  variant={currentView === 'analyze' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('analyze')}
                  className="rounded-md px-3"
                >
                  <Zap className="h-4 w-4 mr-2" />
                  {t('analyzeTab')}
                </Button>
                <Button
                  variant={currentView === 'dashboard' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('dashboard')}
                  className="rounded-md px-3"
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  {t('dashboardTab')}
                </Button>
                <Button
                  variant={currentView === 'history' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('history')}
                  className="rounded-md px-3"
                >
                  <History className="h-4 w-4 mr-2" />
                  {t('historyTab')}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setCurrentView('landing')}
                  className="rounded-md px-3 text-gray-600"
                >
                  Home
                </Button>
              </div>
            </div>
          </div>
        </div>

        {/* Main Content */}
        {currentView === 'dashboard' && (
          <div className="space-y-8">
            <LiveDashboard />
            <FeatureShowcase />
          </div>
        )}

        {currentView === 'history' && (
          <div className="max-w-4xl mx-auto">
            <AnalysisHistory onAnalyzeUrl={(url) => {
              setUrl(url);
              setCurrentView('analyze');
              analyzeWebsite(url);
            }} />
          </div>
        )}

        {currentView === 'analyze' && (
          <>
            {!analysisResult ? (
              <div className="max-w-3xl mx-auto space-y-8">
                <Card className="border-2 border-blue-100 shadow-lg">
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Zap className="h-5 w-5 mr-2 text-blue-600" />
                      {t('websiteAnalysis')}
                    </CardTitle>
                    <CardDescription>
                      {t('analysisDescription')}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
                      <Input
                        type="url"
                        placeholder={t('urlPlaceholder')}
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        disabled={isAnalyzing}
                        className="flex-1 text-base"
                      />
                      <Button 
                        onClick={() => analyzeWebsite()} 
                        disabled={isAnalyzing || !url.trim()}
                        className="px-6 sm:px-8"
                        size="lg"
                      >
                        {isAnalyzing ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                            {t('analyzing')}
                          </>
                        ) : (
                          <>
                            <Sparkles className="h-4 w-4 mr-2" />
                            {t('analyzeButton')}
                          </>
                        )}
                      </Button>
                    </div>

                    {isAnalyzing && (
                      <div className="space-y-3">
                        <div className="flex justify-between text-sm text-gray-600">
                          <span>Analysis Progress</span>
                          <span>{progress}%</span>
                        </div>
                        <Progress value={progress} className="w-full h-3" />
                        <p className="text-sm text-gray-500 text-center">
                          {progress < 30 ? '🔍 Scraping website content...' :
                           progress < 60 ? '🎨 Analyzing design and functionality...' :
                           progress < 90 ? '🤖 Generating AI prompts with Ollama...' :
                           '✨ Finalizing results...'}
                        </p>
                      </div>
                    )}

                    {error && (
                      <Alert variant="destructive">
                        <AlertCircle className="h-4 w-4" />
                        <AlertDescription>{error}</AlertDescription>
                      </Alert>
                    )}

                    <div className="bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-lg border border-blue-200">
                      <h3 className="font-semibold text-blue-900 mb-3 flex items-center">
                        <CheckCircle className="h-5 w-5 mr-2" />
                        What you'll get:
                      </h3>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                        <div className="flex items-center text-blue-800">
                          <Palette className="h-4 w-4 mr-2 text-purple-500" />
                          Design analysis (colors, typography, layout)
                        </div>
                        <div className="flex items-center text-blue-800">
                          <Settings className="h-4 w-4 mr-2 text-green-500" />
                          Functionality breakdown & user flows
                        </div>
                        <div className="flex items-center text-blue-800">
                          <Code className="h-4 w-4 mr-2 text-orange-500" />
                          Technical implementation recommendations
                        </div>
                        <div className="flex items-center text-blue-800">
                          <Users className="h-4 w-4 mr-2 text-rose-500" />
                          Content strategy & UX guidelines
                        </div>
                        <div className="flex items-center text-blue-800 md:col-span-2">
                          <FileText className="h-4 w-4 mr-2 text-blue-500" />
                          Ready-to-use AI prompts in text and JSON formats
                        </div>
                      </div>
                    </div>
                  </CardContent>
                </Card>

                {/* Feature Showcase */}
                <FeatureShowcase />
              </div>
            ) : (
              <div className="space-y-6">
                {/* Success Header */}
                <div className="text-center">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                    <CheckCircle className="h-8 w-8 text-green-600" />
                  </div>
                  <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-2">Analysis Complete!</h2>
                  <p className="text-gray-600">
                    Successfully analyzed <span className="font-semibold text-blue-600">{analysisResult.analysis.website_info.url}</span>
                  </p>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                  <Card className="text-center hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <Globe className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">Website Type</p>
                      <p className="font-semibold capitalize">
                        {analysisResult.analysis.summary.website_type.replace('_', ' ')}
                      </p>
                    </CardContent>
                  </Card>
                  <Card className="text-center hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <Users className="h-8 w-8 text-green-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">Primary Purpose</p>
                      <p className="font-semibold capitalize">
                        {analysisResult.analysis.summary.primary_purpose.replace('_', ' ')}
                      </p>
                    </CardContent>
                  </Card>
                  <Card className="text-center hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <Settings className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">Core Features</p>
                      <p className="font-semibold">
                        {analysisResult.analysis.summary.core_features.length} identified
                      </p>
                    </CardContent>
                  </Card>
                  <Card className="text-center hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <Code className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">Business Type</p>
                      <p className="font-semibold capitalize">
                        {analysisResult.analysis.summary.business_type.replace('_', ' ')}
                      </p>
                    </CardContent>
                  </Card>
                </div>

                {/* Analysis Results */}
                <Card className="border-2 border-gray-100 shadow-lg">
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <BarChart3 className="h-5 w-5 mr-2 text-blue-600" />
                      Analysis Results
                    </CardTitle>
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
                            <h4 className="font-semibold mb-3">Core Features Detected</h4>
                            <div className="space-y-2">
                              {analysisResult.analysis.summary.core_features.map((feature, index) => (
                                <div key={index} className="flex items-center p-2 bg-blue-50 dark:bg-blue-950 rounded-md">
                                  <CheckCircle className="h-4 w-4 mr-2 text-blue-600" />
                                  <span className="text-sm font-medium capitalize">
                                    {feature.replace(/_/g, ' ')}
                                  </span>
                                </div>
                              ))}
                              {analysisResult.analysis.summary.core_features.length === 0 && (
                                <p className="text-sm text-muted-foreground italic">No specific features detected</p>
                              )}
                            </div>
                            
                            {/* Additional Feature Details */}
                            <div className="mt-4">
                              <h5 className="font-medium mb-2 text-sm">Implementation Insights</h5>
                              <div className="space-y-1 text-xs">
                                <div className="flex justify-between">
                                  <span>Interactive Elements:</span>
                                  <Badge variant="outline">
                                    {analysisResult.analysis.functionality_analysis.user_interactions?.interaction_complexity || 'Medium'}
                                  </Badge>
                                </div>
                                <div className="flex justify-between">
                                  <span>Navigation Complexity:</span>
                                  <Badge variant="outline">
                                    {analysisResult.analysis.functionality_analysis.navigation_structure?.navigation_items > 5 ? 'Complex' : 'Simple'}
                                  </Badge>
                                </div>
                                <div className="flex justify-between">
                                  <span>Content Type:</span>
                                  <Badge variant="outline">
                                    {analysisResult.analysis.website_info?.primary_purpose || 'Standard'}
                                  </Badge>
                                </div>
                              </div>
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
                        <div className="bg-gradient-to-r from-gray-50 to-blue-50 p-6 rounded-lg border border-gray-200">
                          <h4 className="font-semibold mb-3 flex items-center">
                            <FileText className="h-5 w-5 mr-2 text-blue-600" />
                            Generated Prompt Preview
                          </h4>
                          <div className="bg-white p-4 rounded-lg border text-sm font-mono max-h-64 overflow-y-auto shadow-inner">
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
                            <div className="space-y-2">
                              <div className="flex items-center p-2 bg-blue-50 rounded">
                                <FileText className="h-4 w-4 mr-2 text-blue-600" />
                                <span>Human-readable text prompt</span>
                              </div>
                              <div className="flex items-center p-2 bg-green-50 rounded">
                                <Code className="h-4 w-4 mr-2 text-green-600" />
                                <span>Structured JSON format</span>
                              </div>
                              <div className="flex items-center p-2 bg-purple-50 rounded">
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

                {/* Enhanced Action Buttons */}
                <div className="flex flex-col sm:flex-row justify-center space-y-2 sm:space-y-0 sm:space-x-4">
                  <Button onClick={downloadResults} size="lg" className="px-8 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700">
                    <Download className="h-4 w-4 mr-2" />
                    Download Results
                  </Button>
                  <Button onClick={resetAnalysis} variant="outline" size="lg" className="px-8 border-2 hover:bg-gray-50">
                    <Sparkles className="h-4 w-4 mr-2" />
                    Analyze Another Website
                  </Button>
                </div>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

function App() {
  return (
    <ThemeProvider>
      <AppContent />
    </ThemeProvider>
  )
}

export default App

