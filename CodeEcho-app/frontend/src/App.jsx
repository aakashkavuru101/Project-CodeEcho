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
  Loader2, 
  CheckCircle, 
  AlertCircle, 
  Code, 
  Palette, 
  Settings, 
  Users, 
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

      const response = await fetch(`${config.API_BASE_URL}/api/demo-repository`, {
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
    setUrl('')
    setError(null)
    setSessionId(null)
    setProgress(0)
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="mb-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              {t('title')}
            </h1>
            <p className="text-xl text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
              {t('subtitle')}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2">
              {t('secureSubtitle')}
            </p>
          </div>

          <div className="flex justify-center mb-8">
            <div className="bg-white dark:bg-gray-800 rounded-lg p-1 shadow-sm border border-gray-200 dark:border-gray-700">
              <nav className="flex space-x-1" role="tablist" aria-label="Application tabs">
                <Button
                  variant={currentView === 'analyze' ? 'default' : 'ghost'}
                  size="sm"
                  onClick={() => setCurrentView('analyze')}
                  className="rounded-md px-3 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800"
                  role="tab"
                  aria-selected={currentView === 'analyze'}
                  aria-controls="analyze-panel"
                >
                  <Sparkles className="h-4 w-4 mr-2" aria-hidden="true" />
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
                      <Sparkles className="h-5 w-5 mr-2 text-blue-600" aria-hidden="true" />
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
                            <Sparkles className="h-4 w-4 mr-2 text-blue-500" />
                            Automatic content generation from README and project data
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

                {/* Repository Details */}
                <Card className="border-2 border-gray-100 shadow-lg">
                  <CardHeader>
                    <CardTitle className="flex items-center">
                      <BarChart3 className="h-5 w-5 mr-2 text-blue-600" />
                      {t('repositoryInfo')}
                    </CardTitle>
                    <CardDescription>
                      Repository analysis and generated website information
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <h4 className="font-semibold mb-3">Repository Information</h4>
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
                        
                        {analysisResult.analysis.tech_stack?.frameworks?.length > 0 && (
                          <div>
                            <h5 className="font-medium mb-2 text-sm">Technologies</h5>
                            <div className="flex flex-wrap gap-1">
                              {analysisResult.analysis.tech_stack.frameworks.slice(0, 6).map((tech, index) => (
                                <Badge key={index} variant="outline" className="text-xs">
                                  {tech}
                                </Badge>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </CardContent>
                </Card>
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