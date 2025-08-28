export const translations = {
  en: {
    // Header and navigation
    title: "CodeEcho",
    subtitle: "AI-powered website analysis with Ollama",
    secureSubtitle: "Secure, local AI processing • 4 specialized models • Comprehensive analysis",
    analyzeTab: "Analyze",
    dashboardTab: "Dashboard", 
    historyTab: "History",
    
    // Landing page
    getStarted: "Get Started",
    aiPoweredAnalysis: "AI-Powered Website Analysis",
    reverseEngineer: "Reverse engineer any website",
    generatePrompts: "Generate comprehensive prompts",
    
    // Analysis page
    websiteAnalysis: "Website Analysis",
    analysisDescription: "Enter a website URL to extract design patterns, functionality, and generate comprehensive AI prompts",
    urlPlaceholder: "https://example.com",
    analyzeButton: "Analyze Website",
    analyzing: "Analyzing...",
    
    // Results
    analysisComplete: "Analysis Complete!",
    downloadResults: "Download Results",
    websiteInfo: "Website Information",
    designAnalysis: "Design Analysis", 
    functionalityAnalysis: "Functionality Analysis",
    technicalAnalysis: "Technical Analysis",
    promptPreview: "Prompt Preview",
    
    // Features
    fourAiModels: "4 AI Models",
    multiModelDesc: "Llama, Qwen, Mistral, and Gemma working together with automatic failover",
    privateProcessing: "100% Private",
    privateDesc: "All processing happens locally with Ollama. Your data never leaves your environment.",
    lightningFast: "Lightning Fast", 
    fastDesc: "Optimized model selection for speed and accuracy. Get results in seconds.",
    designIntelligence: "Design Intelligence",
    designDesc: "Extract color palettes, typography, layouts, and visual hierarchy patterns.",
    
    // Errors
    errorUrlRequired: "Please enter a valid URL",
    errorAnalysisFailed: "Analysis failed",
    errorConnection: "Failed to connect to the analysis service"
  },
  ja: {
    // Header and navigation  
    title: "CodeEcho",
    subtitle: "Ollamaを使用したAI駆動のウェブサイト分析",
    secureSubtitle: "安全なローカルAI処理 • 4つの専門モデル • 包括的な分析",
    analyzeTab: "分析",
    dashboardTab: "ダッシュボード",
    historyTab: "履歴",
    
    // Landing page
    getStarted: "開始する",
    aiPoweredAnalysis: "AI駆動のウェブサイト分析",
    reverseEngineer: "どんなウェブサイトでもリバースエンジニアリング",
    generatePrompts: "包括的なプロンプトを生成",
    
    // Analysis page
    websiteAnalysis: "ウェブサイト分析",
    analysisDescription: "ウェブサイトのURLを入力して、デザインパターン、機能を抽出し、包括的なAIプロンプトを生成します",
    urlPlaceholder: "https://example.com",
    analyzeButton: "ウェブサイトを分析",
    analyzing: "分析中...",
    
    // Results
    analysisComplete: "分析完了！",
    downloadResults: "結果をダウンロード",
    websiteInfo: "ウェブサイト情報",
    designAnalysis: "デザイン分析",
    functionalityAnalysis: "機能分析", 
    technicalAnalysis: "技術分析",
    promptPreview: "プロンプトプレビュー",
    
    // Features
    fourAiModels: "4つのAIモデル",
    multiModelDesc: "Llama、Qwen、Mistral、Gemmaが自動フェイルオーバーで連携",
    privateProcessing: "100%プライベート",
    privateDesc: "すべての処理はOllamaでローカルに行われます。データが環境から離れることはありません。",
    lightningFast: "超高速",
    fastDesc: "速度と精度のために最適化されたモデル選択。数秒で結果を取得。",
    designIntelligence: "デザインインテリジェンス",
    designDesc: "カラーパレット、タイポグラフィ、レイアウト、視覚的階層パターンを抽出。",
    
    // Errors
    errorUrlRequired: "有効なURLを入力してください",
    errorAnalysisFailed: "分析に失敗しました",
    errorConnection: "分析サービスへの接続に失敗しました"
  }
}

export function useTranslation(language) {
  return (key) => {
    return translations[language]?.[key] || translations.en[key] || key
  }
}