import axios from 'axios';
import type {
  PlanningResponse,
  ChatResponse,
  UploadResponse,
  WeekPlanning,
  HistoryResponse
} from '../types';

const api = axios.create({
  baseURL: '/api',
});

// Upload endpoints
export const uploadPdf = async (file: File, processWithAi = true): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post<UploadResponse>(
    `/upload/pdf?process_with_ai=${processWithAi}`,
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );
  return response.data;
};

export const uploadExcel = async (file: File): Promise<UploadResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post<UploadResponse>(
    '/upload/excel',
    formData,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  );
  return response.data;
};

// Planning endpoints
export const getCurrentPlanning = async (): Promise<PlanningResponse> => {
  const response = await api.get<PlanningResponse>('/planning/current');
  return response.data;
};

export const updatePlanning = async (planning: WeekPlanning): Promise<PlanningResponse> => {
  const response = await api.put<PlanningResponse>('/planning/update', planning);
  return response.data;
};

export const generatePlanning = async (
  instructions: string,
  weekNumber?: number,
  year?: number
): Promise<PlanningResponse> => {
  const response = await api.post<PlanningResponse>('/planning/generate', {
    instructions,
    week_number: weekNumber,
    year,
  });
  return response.data;
};

export const aiUpdatePlanning = async (instructions: string): Promise<PlanningResponse> => {
  const response = await api.put<PlanningResponse>('/planning/ai-update', {
    instructions,
  });
  return response.data;
};

export const clearPlanning = async (): Promise<PlanningResponse> => {
  const response = await api.delete<PlanningResponse>('/planning/clear');
  return response.data;
};

// Chat endpoint
export const sendChatMessage = async (message: string): Promise<ChatResponse> => {
  const response = await api.post<ChatResponse>('/chat/message', {
    message,
  });
  return response.data;
};

// Export endpoints
export const exportPdf = (): string => '/api/export/pdf';
export const exportExcel = (): string => '/api/export/excel';

// History endpoint
export const getHistory = async (): Promise<HistoryResponse> => {
  const response = await api.get<HistoryResponse>('/history/');
  return response.data;
};
