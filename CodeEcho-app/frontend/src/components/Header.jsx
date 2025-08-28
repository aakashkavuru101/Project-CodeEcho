import React from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Switch } from '@/components/ui/switch.jsx'
import { Github, Sun, Moon, Languages } from 'lucide-react'
import { useTheme, useLanguage } from '@/contexts/ThemeContext.jsx'
import { useTranslation } from '@/utils/translations.js'

export default function Header() {
  const { theme, toggleTheme } = useTheme()
  const { language, toggleLanguage } = useLanguage()
  const t = useTranslation(language)

  return (
    <header className="border-b bg-white dark:bg-gray-900 backdrop-blur" role="banner">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center space-x-2">
          <h1 className="text-xl font-bold text-blue-600" aria-label="CodeEcho - AI-powered website analysis">{t('title')}</h1>
        </div>

        {/* Controls */}
        <nav className="flex items-center space-x-4" role="navigation" aria-label="Header controls">
          {/* Language Toggle */}
          <div className="flex items-center space-x-2">
            <Languages className="h-4 w-4 text-gray-500 dark:text-gray-400" aria-hidden="true" />
            <Button
              variant="ghost"
              size="sm"
              onClick={toggleLanguage}
              className="text-sm font-medium focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
              aria-label={`Switch to ${language === 'en' ? 'Japanese' : 'English'} language`}
            >
              {language === 'en' ? '日本語' : 'English'}
            </Button>
          </div>

          {/* Theme Toggle */}
          <div className="flex items-center space-x-2">
            <Sun className="h-4 w-4 text-gray-500 dark:text-gray-400" aria-hidden="true" />
            <Switch
              checked={theme === 'dark'}
              onCheckedChange={toggleTheme}
              aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} theme`}
              className="focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
            />
            <Moon className="h-4 w-4 text-gray-500 dark:text-gray-400" aria-hidden="true" />
          </div>

          {/* GitHub Link */}
          <Button
            variant="ghost"
            size="sm"
            asChild
          >
            <a 
              href="https://github.com/aakashkavuru101/Project-CodeEcho"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-900"
              aria-label="View CodeEcho source code on GitHub (opens in new tab)"
            >
              <Github className="h-4 w-4" aria-hidden="true" />
              <span className="hidden sm:inline">GitHub</span>
            </a>
          </Button>
        </nav>
      </div>
    </header>
  )
}