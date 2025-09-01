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
  History,
  Bot
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

  const analyzeRepository = async (repositoryUrl = null) => {
    const targetUrl = repositoryUrl || url;
    if (!targetUrl.trim()) {
      setError(t('errorUrlRequired'))
      return
    }

    // Validate GitHub URL
    if (!targetUrl.toLowerCase().includes('github.com')) {
      setError(t('errorInvalidRepo'))
      return
    }

    setIsAnalyzing(true)
    setError(null)
    setProgress(0)
    setCurrentView('analyze')
    
    try {
      // GitHub-specific progress simulation with realistic steps
      const progressSteps = [
        { progress: 15, message: t('githubConnecting') },
        { progress: 25, message: t('githubFetching') },
        { progress: 45, message: t('githubAnalyzing') },
        { progress: 60, message: t('githubReadme') },
        { progress: 75, message: t('websiteBuilding') },
        { progress: 85, message: t('websitePopulating') },
        { progress: 95, message: t('websiteDeploying') },
        { progress: 100, message: t('websiteFinalizing') }
      ]
      
      let stepIndex = 0
      const progressInterval = setInterval(() => {
        if (stepIndex < progressSteps.length) {
          setProgress(progressSteps[stepIndex].progress)
          stepIndex++
        } else {
          clearInterval(progressInterval)
        }
      }, 800) // Slower progress for better UX

      const response = await fetch(`${config.API_BASE_URL}/api/analyze-repository`, {
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
        setTimeout(() => {
          setIsAnalyzing(false)
          setProgress(0)
        }, 1000) // Brief delay to show completion
      } else {
        throw new Error(data.message || t('errorAnalysisFailed'))
      }
    } catch (error) {
      console.error('Repository analysis error:', error)
      setError(error.message || t('errorConnection'))
      setIsAnalyzing(false)
      setProgress(0)
    }
  }

  const openGeneratedWebsite = () => {
    if (!sessionId) return
    
    const websiteUrl = `${config.API_BASE_URL}/api/website-preview/${sessionId}`
    window.open(websiteUrl, '_blank')
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
    <div className="min-h-screen bg-white dark:bg-gray-900">
      <Header />
      <main className="container mx-auto px-4 py-6 md:py-8" role="main" id="main-content">
        {/* Skip to content link for screen readers */}
        <a 
          href="#main-content" 
          className="sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 z-50 bg-blue-600 text-white px-4 py-2 rounded-md"
        >
          Skip to main content
        </a>
        
        {/* Enhanced Header */}
        <div className="text-center mb-8 md:mb-12">
          <div className="flex items-center justify-center mb-4">
            <div className="relative">
              <Globe className="h-10 w-10 md:h-12 md:w-12 text-blue-600 mr-3" aria-hidden="true" />
              <Sparkles className="h-4 w-4 text-yellow-500 absolute -top-1 -right-1 animate-pulse" aria-hidden="true" />
            </div>
            <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-gray-100">{t('title')}</h1>
          </div>
          <div className="max-w-3xl mx-auto space-y-2">
            <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300">
              {t('subtitle')}
            </p>
            <p className="text-sm md:text-base text-gray-500 dark:text-gray-400">
              {t('secureSubtitle')}
            </p>
          </div>
          
          {/* Navigation Tabs */}
          <div className="mt-6">
            <div className="flex justify-center">
              <nav 
                className="inline-flex rounded-lg border bg-white dark:bg-gray-800 dark:border-gray-700 p-1"
                role="tablist" 
                aria-label="Main navigation"
              >
                <Button
                  variant={currentView === 'analyze' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('analyze')}
                  className="rounded-md px-3 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
                  role="tab"
                  aria-selected={currentView === 'analyze'}
                  aria-controls="analyze-panel"
                >
                  <Zap className="h-4 w-4 mr-2" aria-hidden="true" />
                  {t('analyzeTab')}
                </Button>
                <Button
                  variant={currentView === 'dashboard' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('dashboard')}
                  className="rounded-md px-3 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
                  role="tab"
                  aria-selected={currentView === 'dashboard'}
                  aria-controls="dashboard-panel"
                >
                  <BarChart3 className="h-4 w-4 mr-2" aria-hidden="true" />
                  {t('dashboardTab')}
                </Button>
                <Button
                  variant={currentView === 'history' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('history')}
                  className="rounded-md px-3 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
                  role="tab"
                  aria-selected={currentView === 'history'}
                  aria-controls="history-panel"
                >
                  <History className="h-4 w-4 mr-2" aria-hidden="true" />
                  {t('historyTab')}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setCurrentView('landing')}
                  className="rounded-md px-3 text-gray-600 dark:text-gray-300 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
                  aria-label="Return to home page"
                >
                  Home
                </Button>
              </nav>
            </div>
          </div>
        </div>

        {/* Main Content */}
        {currentView === 'dashboard' && (
          <div className="space-y-8" role="tabpanel" id="dashboard-panel" aria-labelledby="dashboard-tab">
            <LiveDashboard />
            <FeatureShowcase />
          </div>
        )}

        {currentView === 'history' && (
          <div className="max-w-4xl mx-auto" role="tabpanel" id="history-panel" aria-labelledby="history-tab">
            <AnalysisHistory onAnalyzeUrl={(url) => {
              setUrl(url);
              setCurrentView('analyze');
              analyzeRepository(url);
            }} />
          </div>
        )}

        {currentView === 'analyze' && (
          <div role="tabpanel" id="analyze-panel" aria-labelledby="analyze-tab">
            {!analysisResult ? (
              <div className="max-w-3xl mx-auto space-y-8">
                <Card className="border-2 border-blue-100 shadow-lg">
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <Zap className="h-5 w-5 mr-2 text-blue-600" aria-hidden="true" />
                      {t('websiteAnalysis')}
                    </CardTitle>
                    <CardDescription>
                      {t('analysisDescription')}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <form onSubmit={(e) => { e.preventDefault(); analyzeRepository(); }} className="flex flex-col sm:flex-row space-y-2 sm:space-y-0 sm:space-x-2">
                      <Input
                        type="url"
                        placeholder={t('urlPlaceholder')}
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                        disabled={isAnalyzing}
                        className="flex-1 text-base"
                        aria-label="GitHub repository URL to analyze"
                        aria-describedby="url-help"
                        required
                      />
                      <Button 
                        type="submit"
                        disabled={isAnalyzing || !url.trim()}
                        className="px-6 sm:px-8"
                        size="lg"
                        aria-describedby={isAnalyzing ? "analyzing-status" : undefined}
                      >
                        {isAnalyzing ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-2 animate-spin" aria-hidden="true" />
                            {t('analyzing')}
                          </>
                        ) : (
                          <>
                            <Sparkles className="h-4 w-4 mr-2" aria-hidden="true" />
                            {t('analyzeButton')}
                          </>
                        )}
                      </Button>
                    </form>
                    <div id="url-help" className="sr-only">
                      Enter a complete GitHub repository URL including https://github.com/
                    </div>

                    {isAnalyzing && (
                      <div className="space-y-3" role="status" aria-live="polite" id="analyzing-status">
                        <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400">
                          <span>Analysis Progress</span>
                          <span>{progress}%</span>
                        </div>
                        <Progress value={progress} className="w-full h-3" aria-label={`Analysis progress: ${progress}%`} />
                        <p className="text-sm text-gray-500 dark:text-gray-400 text-center">
                          {progress < 20 ? '🔗 Connecting to GitHub API...' :
                           progress < 30 ? '📦 Fetching repository data...' :
                           progress < 50 ? '🔍 Analyzing code and identifying framework...' :
                           progress < 65 ? '📖 Parsing README.md for project description...' :
                           progress < 80 ? '🏗️ Building project website from template...' :
                           progress < 90 ? '📝 Populating content: project name, description, and tech stack...' :
                           progress < 100 ? '🚀 Preparing deployment-ready website...' :
                           '✨ Finalizing... Almost there!'}
                        </p>
                      </div>
                    )}

                    {error && (
                      <Alert variant="destructive" role="alert">
                        <AlertCircle className="h-4 w-4" aria-hidden="true" />
                        <AlertDescription>{error}</AlertDescription>
                      </Alert>
                    )}

                      <div className="bg-gradient-to-r from-gray-50 to-blue-50 p-6 rounded-lg border border-gray-200">
                        <h3 className="font-semibold text-blue-900 mb-3 flex items-center">
                          <CheckCircle className="h-5 w-5 mr-2" />
                          What you'll get:
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
                          <div className="flex items-center text-blue-800">
                            <Code className="h-4 w-4 mr-2 text-purple-500" />
                            Complete repository analysis with tech stack detection
                          </div>
                          <div className="flex items-center text-blue-800">
                            <Palette className="h-4 w-4 mr-2 text-green-500" />
                            Beautiful, responsive portfolio website
                          </div>
                          <div className="flex items-center text-blue-800">
                            <Settings className="h-4 w-4 mr-2 text-orange-500" />
                            Professional templates tailored to your project
                          </div>
                          <div className="flex items-center text-blue-800">
                            <Users className="h-4 w-4 mr-2 text-rose-500" />
                            Deployment-ready static website
                          </div>
                          <div className="flex items-center text-blue-800 md:col-span-2">
                            <FileText className="h-4 w-4 mr-2 text-blue-500" />
                            Automatic content generation from README and project data
                          </div>
                          <div className="flex items-center text-blue-800 md:col-span-2">
                            <Bot className="h-4 w-4 mr-2 text-purple-500" />
                            Powered by 8 specialized AI models for maximum accuracy
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
                  <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-2">{t('analysisComplete')}</h2>
                  <p className="text-gray-600">
                    Successfully generated website for <span className="font-semibold text-blue-600">{analysisResult.analysis.repository_info?.name || 'repository'}</span>
                    {analysisResult.from_cache && (
                      <span className="ml-2 inline-flex items-center px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full">
                        ⚡ {t('successCached')}
                      </span>
                    )}
                  </p>
                </div>

                {/* Quick Stats */}
                <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
                  <Card className="text-center hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <Code className="h-8 w-8 text-blue-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">Primary Language</p>
                      <p className="font-semibold">
                        {analysisResult.analysis.repository_info?.language || 'Multiple'}
                      </p>
                    </CardContent>
                  </Card>
                  <Card className="text-center hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <Users className="h-8 w-8 text-green-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">Project Type</p>
                      <p className="font-semibold capitalize">
                        {t(`projectTypes.${analysisResult.analysis.project_analysis?.project_type}`) || 
                         analysisResult.analysis.project_analysis?.project_type?.replace('_', ' ') || 'General'}
                      </p>
                    </CardContent>
                  </Card>
                  <Card className="text-center hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <Settings className="h-8 w-8 text-purple-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">Complexity</p>
                      <p className="font-semibold">
                        {t(`complexityLevels.${analysisResult.analysis.project_analysis?.complexity_level}`) ||
                         analysisResult.analysis.project_analysis?.complexity_level || 'Medium'}
                      </p>
                    </CardContent>
                  </Card>
                  <Card className="text-center hover:shadow-md transition-shadow">
                    <CardContent className="p-4">
                      <Globe className="h-8 w-8 text-orange-600 mx-auto mb-2" />
                      <p className="text-sm text-gray-600">Stars</p>
                      <p className="font-semibold">
                        {analysisResult.analysis.repository_info?.stars || 0}
                      </p>
                    </CardContent>
                  </Card>
                </div>

                {/* Action Buttons */}
                <div className="flex flex-col sm:flex-row gap-3 justify-center">
                  <Button 
                    onClick={openGeneratedWebsite}
                    className="flex items-center gap-2 px-6 py-3"
                    size="lg"
                  >
                    <Globe className="h-5 w-5" />
                    {t('viewWebsite')}
                  </Button>
                  <Button 
                    variant="outline"
                    onClick={() => {
                      setAnalysisResult(null)
                      setUrl('')
                      setError(null)
                    }}
                    className="flex items-center gap-2 px-6 py-3"
                    size="lg"
                  >
                    <Sparkles className="h-5 w-5" />
                    Generate Another
                  </Button>
                </div>

                {/* Analysis Results */}
                <Card className="border-2 border-gray-100 shadow-lg">
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <BarChart3 className="h-5 w-5 mr-2 text-blue-600" />
                      {t('repositoryInfo')}
                    </CardTitle>
                    <CardDescription>
                      Detailed analysis of the GitHub repository and generated website information
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Tabs defaultValue="repository" className="w-full">
                      <TabsList className="grid w-full grid-cols-4">
                        <TabsTrigger value="repository">Repository</TabsTrigger>
                        <TabsTrigger value="techstack">{t('techStack')}</TabsTrigger>
                        <TabsTrigger value="analysis">{t('projectAnalysis')}</TabsTrigger>
                        <TabsTrigger value="website">{t('websitePreview')}</TabsTrigger>
                      </TabsList>

                      <TabsContent value="repository" className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <h4 className="font-semibold mb-2">Repository Information</h4>
                            <div className="space-y-2 text-sm">
                              <div className="flex justify-between">
                                <span className="text-gray-600">Name:</span>
                                <Badge variant="secondary">
                                  {analysisResult.analysis.repository_info?.name || 'Unknown'}
                                </Badge>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Language:</span>
                                <span>{analysisResult.analysis.repository_info?.language || 'Multiple'}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Stars:</span>
                                <span>{analysisResult.analysis.repository_info?.stars || 0}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Forks:</span>
                                <span>{analysisResult.analysis.repository_info?.forks || 0}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">License:</span>
                                <span>{analysisResult.analysis.repository_info?.license || 'Unknown'}</span>
                              </div>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-semibold mb-3">Description</h4>
                            <p className="text-sm text-gray-600 mb-4">
                              {analysisResult.analysis.repository_info?.description || 'No description available'}
                            </p>
                            
                            {analysisResult.analysis.repository_info?.topics?.length > 0 && (
                              <div>
                                <h5 className="font-medium mb-2 text-sm">Topics</h5>
                                <div className="flex flex-wrap gap-1">
                                  {analysisResult.analysis.repository_info.topics.map((topic, index) => (
                                    <Badge key={index} variant="outline" className="text-xs">
                                      {topic}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                            )}

                            {analysisResult.analysis.repository_info?.homepage && (
                              <div className="mt-4">
                                <h5 className="font-medium mb-2 text-sm">Homepage</h5>
                                <a 
                                  href={analysisResult.analysis.repository_info.homepage}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-600 hover:text-blue-800 underline text-sm"
                                >
                                  {analysisResult.analysis.repository_info.homepage}
                                </a>
                              </div>
                            )}
                          </div>
                        </div>
                      </TabsContent>

                      <TabsContent value="techstack" className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <h4 className="font-semibold mb-2 flex items-center">
                              <Code className="h-4 w-4 mr-2" />
                              Programming Languages
                            </h4>
                            <div className="space-y-2">
                              {analysisResult.analysis.tech_stack?.languages?.length > 0 ? (
                                analysisResult.analysis.tech_stack.languages.map((lang, index) => (
                                  <Badge key={index} variant="secondary" className="mr-2 mb-2">
                                    {lang}
                                  </Badge>
                                ))
                              ) : (
                                <p className="text-sm text-gray-500">No languages detected</p>
                              )}
                            </div>
                          </div>
                          <div>
                            <h4 className="font-semibold mb-2">Frameworks & Tools</h4>
                            <div className="space-y-2">
                              {analysisResult.analysis.tech_stack?.frameworks?.length > 0 ? (
                                analysisResult.analysis.tech_stack.frameworks.map((framework, index) => (
                                  <Badge key={index} variant="outline" className="mr-2 mb-2">
                                    {framework}
                                  </Badge>
                                ))
                              ) : (
                                <p className="text-sm text-gray-500">No frameworks detected</p>
                              )}
                            </div>
                          </div>
                        </div>
                        
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                          <div>
                            <h4 className="font-semibold mb-2">Deployment</h4>
                            <div className="space-y-2">
                              {analysisResult.analysis.tech_stack?.deployment?.length > 0 ? (
                                analysisResult.analysis.tech_stack.deployment.map((deploy, index) => (
                                  <Badge key={index} variant="outline" className="mr-2 mb-2">
                                    {deploy}
                                  </Badge>
                                ))
                              ) : (
                                <p className="text-sm text-gray-500">No deployment tools detected</p>
                              )}
                            </div>
                          </div>
                          <div>
                            <h4 className="font-semibold mb-2">Databases</h4>
                            <div className="space-y-2">
                              {analysisResult.analysis.tech_stack?.databases?.length > 0 ? (
                                analysisResult.analysis.tech_stack.databases.map((db, index) => (
                                  <Badge key={index} variant="outline" className="mr-2 mb-2">
                                    {db}
                                  </Badge>
                                ))
                              ) : (
                                <p className="text-sm text-gray-500">No databases detected</p>
                              )}
                            </div>
                          </div>
                        </div>
                      </TabsContent>

                      <TabsContent value="analysis" className="space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <h4 className="font-semibold mb-2">Project Analysis</h4>
                            <div className="space-y-2 text-sm">
                              <div className="flex justify-between">
                                <span className="text-gray-600">Type:</span>
                                <Badge variant="secondary">
                                  {t(`projectTypes.${analysisResult.analysis.project_analysis?.project_type}`) || 
                                   analysisResult.analysis.project_analysis?.project_type?.replace('_', ' ') || 'General'}
                                </Badge>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Complexity:</span>
                                <Badge variant="outline">
                                  {t(`complexityLevels.${analysisResult.analysis.project_analysis?.complexity_level}`) ||
                                   analysisResult.analysis.project_analysis?.complexity_level || 'Medium'}
                                </Badge>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Category:</span>
                                <span>{analysisResult.analysis.project_analysis?.project_category || 'General'}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Status:</span>
                                <Badge variant={analysisResult.analysis.project_analysis?.development_status === 'active' ? 'default' : 'secondary'}>
                                  {analysisResult.analysis.project_analysis?.development_status || 'Unknown'}
                                </Badge>
                              </div>
                            </div>
                          </div>
                          <div>
                            <h4 className="font-semibold mb-2">Website Generation</h4>
                            <div className="space-y-2 text-sm">
                              <div className="flex justify-between">
                                <span className="text-gray-600">Template:</span>
                                <Badge variant="secondary">
                                  {analysisResult.analysis.website_generation?.template_recommendation || 'Clean Minimal'}
                                </Badge>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Color Scheme:</span>
                                <span>{analysisResult.analysis.website_generation?.color_scheme || 'Modern Minimal'}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Layout Style:</span>
                                <span>{analysisResult.analysis.website_generation?.layout_style || 'Balanced'}</span>
                              </div>
                              <div className="flex justify-between">
                                <span className="text-gray-600">Deployment Ready:</span>
                                <Badge variant={analysisResult.analysis.project_analysis?.deployment_ready ? 'default' : 'secondary'}>
                                  {analysisResult.analysis.project_analysis?.deployment_ready ? 'Yes' : 'No'}
                                </Badge>
                              </div>
                            </div>
                          </div>
                        </div>
                      </TabsContent>

                      <TabsContent value="website" className="space-y-4">
                        <div className="text-center">
                          <h4 className="font-semibold mb-4">Generated Website Preview</h4>
                          <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg p-8">
                            <Globe className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                            <p className="text-gray-600 mb-4">
                              Your website has been generated and is ready to view!
                            </p>
                            <Button 
                              onClick={openGeneratedWebsite}
                              className="flex items-center gap-2 mx-auto"
                              size="lg"
                            >
                              <Globe className="h-5 w-5" />
                              Open Website in New Tab
                            </Button>
                          </div>
                          
                          <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                            <div className="bg-blue-50 p-4 rounded-lg">
                              <h5 className="font-medium text-blue-900 mb-2">Template Used</h5>
                              <p className="text-blue-700">
                                {analysisResult.website?.template_type || 'Clean Minimal'}
                              </p>
                            </div>
                            <div className="bg-green-50 p-4 rounded-lg">
                              <h5 className="font-medium text-green-900 mb-2">Color Scheme</h5>
                              <p className="text-green-700">
                                {analysisResult.website?.color_scheme || 'Modern Minimal'}
                              </p>
                            </div>
                            <div className="bg-purple-50 p-4 rounded-lg">
                              <h5 className="font-medium text-purple-900 mb-2">Generated At</h5>
                              <p className="text-purple-700">
                                {analysisResult.website?.generated_at ? 
                                  new Date(analysisResult.website.generated_at).toLocaleString() : 
                                  'Just now'}
                              </p>
                            </div>
                          </div>
                        </div>
                      </TabsContent>
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

                {/* These actions were already added in the earlier success section, so remove this duplicate */}
              </div>
            )}
          </div>
        )}

        {/* Landing Page */}
        {currentView === 'landing' && (
          <LandingPage onGetStarted={() => setCurrentView('analyze')} />
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

