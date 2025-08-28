import React, { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { 
  TrendingUp, 
  Activity, 
  Zap, 
  Users,
  Globe,
  Code,
  Palette
} from 'lucide-react'

export default function LiveDashboard() {
  const [stats, setStats] = useState({
    totalAnalyses: 1247,
    activeModels: 4,
    avgAccuracy: 93,
    successRate: 98.5
  });

  const [modelStatus, setModelStatus] = useState([
    { name: 'Llama 3.1', status: 'active', load: 85, responseTime: 1.2 },
    { name: 'Qwen 2.5', status: 'standby', load: 23, responseTime: 0.9 },
    { name: 'Mistral', status: 'standby', load: 15, responseTime: 0.8 },
    { name: 'Gemma 2', status: 'standby', load: 31, responseTime: 1.5 }
  ]);

  const [recentActivity, setRecentActivity] = useState([
    { type: 'analysis', site: 'ecommerce', time: '2 min ago', status: 'completed' },
    { type: 'model_switch', from: 'llama3.1', to: 'qwen2.5', time: '5 min ago' },
    { type: 'analysis', site: 'portfolio', time: '8 min ago', status: 'completed' },
    { type: 'analysis', site: 'blog', time: '12 min ago', status: 'completed' }
  ]);

  // Simulate live updates
  useEffect(() => {
    const interval = setInterval(() => {
      setStats(prev => ({
        ...prev,
        totalAnalyses: prev.totalAnalyses + Math.floor(Math.random() * 3),
        avgAccuracy: Math.max(90, Math.min(100, prev.avgAccuracy + (Math.random() - 0.5) * 2))
      }));

      setModelStatus(prev => prev.map(model => ({
        ...model,
        load: Math.max(10, Math.min(100, model.load + (Math.random() - 0.5) * 10)),
        responseTime: Math.max(0.5, Math.min(3, model.responseTime + (Math.random() - 0.5) * 0.2))
      })));
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const getActivityIcon = (type) => {
    switch (type) {
      case 'analysis':
        return <Globe className="h-4 w-4 text-blue-500" />;
      case 'model_switch':
        return <Activity className="h-4 w-4 text-purple-500" />;
      default:
        return <Zap className="h-4 w-4 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'bg-green-500';
      case 'standby':
        return 'bg-yellow-500';
      case 'offline':
        return 'bg-red-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full">
      {/* System Stats */}
      <Card className="lg:col-span-2">
        <CardHeader>
          <CardTitle className="flex items-center">
            <TrendingUp className="h-5 w-5 mr-2 text-green-600" />
            System Performance
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{stats.totalAnalyses.toLocaleString()}</div>
              <div className="text-sm text-gray-600">Total Analyses</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{stats.activeModels}</div>
              <div className="text-sm text-gray-600">Active Models</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{stats.avgAccuracy.toFixed(1)}%</div>
              <div className="text-sm text-gray-600">Avg Accuracy</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-600">{stats.successRate}%</div>
              <div className="text-sm text-gray-600">Success Rate</div>
            </div>
          </div>

          {/* Model Status */}
          <div className="space-y-3">
            <h4 className="font-medium text-gray-900">AI Model Status</h4>
            {modelStatus.map((model, index) => (
              <div key={index} className="flex items-center justify-between p-3 rounded-lg bg-gray-50">
                <div className="flex items-center space-x-3">
                  <div className={`w-2 h-2 rounded-full ${getStatusColor(model.status)}`} />
                  <div>
                    <div className="font-medium text-sm">{model.name}</div>
                    <div className="text-xs text-gray-600">
                      {model.responseTime.toFixed(1)}s response time
                    </div>
                  </div>
                </div>
                <div className="text-right min-w-0 flex-1 ml-4">
                  <div className="text-sm font-medium">{model.load.toFixed(0)}% load</div>
                  <Progress value={model.load} className="h-1 mt-1" />
                </div>
                <Badge 
                  variant={model.status === 'active' ? 'default' : 'secondary'}
                  className="ml-2 text-xs"
                >
                  {model.status}
                </Badge>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center">
            <Activity className="h-5 w-5 mr-2 text-blue-600" />
            Recent Activity
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-start space-x-3 p-2 rounded hover:bg-gray-50">
                {getActivityIcon(activity.type)}
                <div className="flex-1 min-w-0">
                  <div className="text-sm">
                    {activity.type === 'analysis' && (
                      <>Analyzed <span className="font-medium">{activity.site}</span> website</>
                    )}
                    {activity.type === 'model_switch' && (
                      <>Switched from <span className="font-medium">{activity.from}</span> to <span className="font-medium">{activity.to}</span></>
                    )}
                  </div>
                  <div className="text-xs text-gray-500">{activity.time}</div>
                </div>
                {activity.status && (
                  <Badge variant="outline" className="text-xs">
                    {activity.status}
                  </Badge>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}