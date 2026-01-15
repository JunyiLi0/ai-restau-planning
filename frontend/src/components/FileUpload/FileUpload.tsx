import { useState, useCallback } from 'react';
import { Upload, FileText, FileSpreadsheet } from 'lucide-react';
import { uploadPdf, uploadExcel } from '../../services/api';

interface FileUploadProps {
  onUploadSuccess: () => void;
}

export function FileUpload({ onUploadSuccess }: FileUploadProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(async (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      await handleFile(file);
    }
  }, []);

  const handleFileSelect = useCallback(async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      await handleFile(file);
    }
  }, []);

  const handleFile = async (file: File) => {
    setError(null);
    setIsUploading(true);

    try {
      const fileName = file.name.toLowerCase();

      if (fileName.endsWith('.pdf')) {
        await uploadPdf(file, true);
      } else if (fileName.endsWith('.xlsx') || fileName.endsWith('.xls')) {
        await uploadExcel(file);
      } else {
        setError('Veuillez importer un fichier PDF ou Excel');
        setIsUploading(false);
        return;
      }

      onUploadSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de l\'import');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-4">
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          isDragging
            ? 'border-blue-500 bg-blue-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          accept=".pdf,.xlsx,.xls"
          onChange={handleFileSelect}
          disabled={isUploading}
        />

        <label
          htmlFor="file-upload"
          className="cursor-pointer flex flex-col items-center gap-3"
        >
          <div className="p-3 bg-gray-100 rounded-full">
            <Upload className="w-8 h-8 text-gray-500" />
          </div>
          <div>
            <p className="text-lg font-medium text-gray-700">
              {isUploading ? 'Import en cours...' : 'Déposez votre fichier ici ou cliquez pour parcourir'}
            </p>
            <p className="text-sm text-gray-500 mt-1">
              Fichiers PDF et Excel acceptés
            </p>
          </div>
        </label>

        <div className="flex justify-center gap-4 mt-4">
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <FileText className="w-4 h-4" />
            <span>PDF</span>
          </div>
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <FileSpreadsheet className="w-4 h-4" />
            <span>Excel</span>
          </div>
        </div>
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
          {error}
        </div>
      )}
    </div>
  );
}
