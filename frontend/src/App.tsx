import { useState, useEffect, useCallback } from 'react';
import { Calendar, MessageSquare, Upload, Clock } from 'lucide-react';
import { ChatUI } from './components/ChatUI';
import { FileUpload } from './components/FileUpload';
import { PlanningView } from './components/Planning';
import { History } from './components/History';
import { getCurrentPlanning } from './services/api';
import type { WeekPlanning } from './types';

type Tab = 'chat' | 'upload' | 'history';

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('chat');
  const [planning, setPlanning] = useState<WeekPlanning | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const fetchPlanning = useCallback(async () => {
    try {
      const response = await getCurrentPlanning();
      if (response.success && response.data) {
        setPlanning(response.data);
      } else {
        setPlanning(null);
      }
    } catch (error) {
      console.error('Error fetching planning:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPlanning();
  }, [fetchPlanning]);

  const handlePlanningUpdate = () => {
    fetchPlanning();
  };

  const handleClearPlanning = () => {
    setPlanning(null);
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  // Mode plein écran
  if (isFullscreen && planning) {
    return (
      <div className="min-h-screen bg-gray-100 p-4">
        <PlanningView
          planning={planning}
          onClear={handleClearPlanning}
          isFullscreen={true}
          onToggleFullscreen={toggleFullscreen}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center gap-3">
            <Calendar className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-800">
                Planning WOK10
              </h1>
              <p className="text-sm text-gray-500">
                Gestion automatique des plannings employés
              </p>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Panel - Chat/Upload */}
          <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
            {/* Tabs */}
            <div className="flex border-b">
              <button
                onClick={() => setActiveTab('chat')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'chat'
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <MessageSquare className="w-4 h-4" />
                Chat
              </button>
              <button
                onClick={() => setActiveTab('upload')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'upload'
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Upload className="w-4 h-4" />
                Importer
              </button>
              <button
                onClick={() => setActiveTab('history')}
                className={`flex-1 flex items-center justify-center gap-2 px-4 py-3 text-sm font-medium transition-colors ${
                  activeTab === 'history'
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Clock className="w-4 h-4" />
                Historique
              </button>
            </div>

            {/* Tab Content */}
            <div className="h-[500px] overflow-y-auto">
              {activeTab === 'chat' && (
                <ChatUI onPlanningUpdate={handlePlanningUpdate} />
              )}
              {activeTab === 'upload' && (
                <div className="p-4">
                  <FileUpload onUploadSuccess={handlePlanningUpdate} />
                </div>
              )}
              {activeTab === 'history' && (
                <History />
              )}
            </div>
          </div>

          {/* Right Panel - Planning View */}
          <div className="bg-white rounded-lg shadow-sm border p-4">
            <h2 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
              <Calendar className="w-5 h-5 text-blue-600" />
              Planning actuel
            </h2>

            {isLoading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600" />
              </div>
            ) : planning ? (
              <PlanningView
                planning={planning}
                onClear={handleClearPlanning}
                isFullscreen={false}
                onToggleFullscreen={toggleFullscreen}
              />
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Calendar className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                <p className="text-lg font-medium">Aucun planning chargé</p>
                <p className="text-sm mt-2">
                  Importez un fichier ou utilisez le chat pour créer un planning.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
