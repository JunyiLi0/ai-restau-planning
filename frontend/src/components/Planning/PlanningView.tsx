import { FileText, FileSpreadsheet, Trash2, Maximize2, Minimize2 } from 'lucide-react';
import type { WeekPlanning } from '../../types';
import { getWeekDates } from '../../types';
import { PlanningTable } from './PlanningTable';
import { exportPdf, exportExcel, clearPlanning } from '../../services/api';

interface PlanningViewProps {
  planning: WeekPlanning;
  onClear: () => void;
  isFullscreen?: boolean;
  onToggleFullscreen?: () => void;
}

export function PlanningView({ planning, onClear, isFullscreen = false, onToggleFullscreen }: PlanningViewProps) {
  const handleExportPdf = () => {
    window.open(exportPdf(), '_blank');
  };

  const handleExportExcel = () => {
    window.open(exportExcel(), '_blank');
  };

  const handleClear = async () => {
    if (confirm('Voulez-vous vraiment effacer le planning actuel ?')) {
      await clearPlanning();
      onClear();
    }
  };

  // Calculer les dates de la semaine
  const dates = getWeekDates(planning.week_number, planning.year);

  return (
    <div className={`space-y-4 ${isFullscreen ? 'bg-white rounded-lg shadow-lg p-6' : ''}`}>
      <div className="flex items-center justify-between">
        <h2 className={`font-semibold text-gray-800 ${isFullscreen ? 'text-2xl' : 'text-xl'}`}>
          {dates.start} au {dates.end}
        </h2>
        <div className="flex gap-2">
          {onToggleFullscreen && (
            <button
              onClick={onToggleFullscreen}
              className="flex items-center gap-2 px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
              title={isFullscreen ? 'Quitter le plein écran' : 'Plein écran'}
            >
              {isFullscreen ? (
                <>
                  <Minimize2 className="w-4 h-4" />
                  Réduire
                </>
              ) : (
                <>
                  <Maximize2 className="w-4 h-4" />
                  Agrandir
                </>
              )}
            </button>
          )}
          <button
            onClick={handleExportPdf}
            className="flex items-center gap-2 px-3 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors text-sm"
          >
            <FileText className="w-4 h-4" />
            PDF
          </button>
          <button
            onClick={handleExportExcel}
            className="flex items-center gap-2 px-3 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors text-sm"
          >
            <FileSpreadsheet className="w-4 h-4" />
            Excel
          </button>
          <button
            onClick={handleClear}
            className="flex items-center gap-2 px-3 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm"
          >
            <Trash2 className="w-4 h-4" />
            Effacer
          </button>
        </div>
      </div>

      <div className={`bg-white rounded-lg shadow-sm border p-4 ${isFullscreen ? 'overflow-auto' : ''}`}>
        {planning.employees.length > 0 ? (
          <PlanningTable planning={planning} />
        ) : (
          <p className="text-gray-500 text-center py-8">
            Aucun employé dans le planning. Utilisez le chat pour ajouter des employés.
          </p>
        )}
      </div>

      <div className="text-sm text-gray-500">
        <p>
          <strong>Légende :</strong> Midi = Horaires service midi, Soir = Horaires service soir, Repas = Nombre de repas
        </p>
      </div>
    </div>
  );
}
