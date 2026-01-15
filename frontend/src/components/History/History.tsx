import { useState, useEffect } from 'react';
import { Clock, FileText, FileSpreadsheet, Download, Upload, RefreshCw } from 'lucide-react';
import { getHistory } from '../../services/api';
import type { HistoryEntry, HistoryEntryType } from '../../types';

export function History() {
  const [entries, setEntries] = useState<HistoryEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchHistory = async () => {
    setIsLoading(true);
    try {
      const response = await getHistory();
      if (response.success) {
        setEntries(response.entries);
      }
    } catch (error) {
      console.error('Error fetching history:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const getTypeIcon = (type: HistoryEntryType) => {
    switch (type) {
      case 'import_pdf':
        return <Upload className="w-4 h-4 text-red-500" />;
      case 'import_excel':
        return <Upload className="w-4 h-4 text-green-500" />;
      case 'export_pdf':
        return <Download className="w-4 h-4 text-red-500" />;
      case 'export_excel':
        return <Download className="w-4 h-4 text-green-500" />;
    }
  };

  const getTypeLabel = (type: HistoryEntryType) => {
    switch (type) {
      case 'import_pdf':
        return 'Import PDF';
      case 'import_excel':
        return 'Import Excel';
      case 'export_pdf':
        return 'Export PDF';
      case 'export_excel':
        return 'Export Excel';
    }
  };

  const getFileIcon = (type: HistoryEntryType) => {
    if (type.includes('pdf')) {
      return <FileText className="w-5 h-5 text-red-500" />;
    }
    return <FileSpreadsheet className="w-5 h-5 text-green-500" />;
  };

  return (
    <div className="p-4 space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-800 flex items-center gap-2">
          <Clock className="w-5 h-5 text-blue-600" />
          Historique
        </h3>
        <button
          onClick={fetchHistory}
          className="flex items-center gap-2 px-3 py-1.5 text-sm text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
          disabled={isLoading}
        >
          <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          Actualiser
        </button>
      </div>

      {isLoading ? (
        <div className="flex items-center justify-center py-8">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600" />
        </div>
      ) : entries.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <Clock className="w-12 h-12 mx-auto mb-3 text-gray-300" />
          <p>Aucun historique</p>
          <p className="text-sm mt-1">Les imports et exports apparaitront ici</p>
        </div>
      ) : (
        <div className="space-y-2">
          {entries.map((entry) => (
            <div
              key={entry.id}
              className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <div className="flex-shrink-0">
                {getFileIcon(entry.type)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  {getTypeIcon(entry.type)}
                  <span className="text-sm font-medium text-gray-700">
                    {getTypeLabel(entry.type)}
                  </span>
                </div>
                <p className="text-sm text-gray-600 truncate" title={entry.filename}>
                  {entry.filename}
                </p>
                {entry.week_number && entry.year && (
                  <p className="text-xs text-gray-400">
                    Semaine {entry.week_number}, {entry.year}
                  </p>
                )}
              </div>
              <div className="flex-shrink-0 text-xs text-gray-400">
                {entry.timestamp}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
