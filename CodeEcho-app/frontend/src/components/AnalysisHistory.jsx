import React, { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  XCircle,
  RefreshCw,
  Download,
  ExternalLink
} from 'lucide-react'

export default function AnalysisHistory({ onAnalyzeUrl }) {
  const [history, setHistory] = useState([
    {
      id: 1,
      url: 'https://github.com',
      status: 'completed',
      timestamp: '2024-01-15 14:30',
      type: 'Developer Platform',
      score: 95,
      downloadable: true
    },
    {
      id: 2,
      url: 'https://stripe.com',
      status: 'completed',
      timestamp: '2024-01-15 13:45',
      type: 'SaaS Platform',
      score: 92,
      downloadable: true
    },
    {
      id: 3,
      url: 'https://tailwindcss.com',
      status: 'processing',
      timestamp: '2024-01-15 15:00',
      type: 'Documentation',
      score: 0,
      downloadable: false
    },
    {
      id: 4,
      url: 'https://vercel.com',
      status: 'failed',
      timestamp: '2024-01-15 12:20',
      type: 'Cloud Platform',
      score: 0,
      downloadable: false
    }
  ]);

  const getStatusIcon = (status) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'processing':
        return <RefreshCw className="h-5 w-5 text-blue-500 animate-spin" />;
      case 'failed':
        return <XCircle className="h-5 w-5 text-red-500" />;
      default:
        return <AlertCircle className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusBadge = (status) => {
    const variants = {
      completed: 'default',
      processing: 'secondary',
      failed: 'destructive'
    };
    return (
      <Badge variant={variants[status] || 'outline'} className="capitalize">
        {status}
      </Badge>
    );
  };

  const handleReAnalyze = (url) => {
    if (onAnalyzeUrl) {
      onAnalyzeUrl(url);
    }
  };

  const mockDownload = (id) => {
    // Mock download functionality
    console.log(`Downloading analysis for ID: ${id}`);
  };

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center">
          <Clock className="h-5 w-5 mr-2 text-blue-600" />
          Recent Analysis History
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {history.map((item) => (
            <div 
              key={item.id}
              className="flex items-center justify-between p-4 rounded-lg border bg-gray-50/50 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center space-x-4 flex-1">
                {getStatusIcon(item.status)}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="font-medium text-sm truncate">{item.url}</span>
                    <ExternalLink className="h-3 w-3 text-gray-400 flex-shrink-0" />
                  </div>
                  <div className="flex items-center space-x-2 text-xs text-gray-500">
                    <span>{item.timestamp}</span>
                    <span>•</span>
                    <span>{item.type}</span>
                    {item.status === 'completed' && (
                      <>
                        <span>•</span>
                        <span className="text-green-600 font-medium">Score: {item.score}%</span>
                      </>
                    )}
                  </div>
                  {item.status === 'processing' && (
                    <Progress value={65} className="mt-2 h-1" />
                  )}
                </div>
              </div>
              
              <div className="flex items-center space-x-2">
                {getStatusBadge(item.status)}
                
                {item.status === 'completed' && item.downloadable && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => mockDownload(item.id)}
                    className="h-8 px-2"
                  >
                    <Download className="h-3 w-3" />
                  </Button>
                )}
                
                {item.status === 'failed' && (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => handleReAnalyze(item.url)}
                    className="h-8 px-2"
                  >
                    <RefreshCw className="h-3 w-3" />
                  </Button>
                )}
              </div>
            </div>
          ))}
        </div>
        
        {history.length === 0 && (
          <div className="text-center py-8 text-gray-500">
            <Clock className="h-12 w-12 mx-auto mb-4 text-gray-300" />
            <p>No analysis history yet</p>
            <p className="text-sm">Start by analyzing your first website above</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}