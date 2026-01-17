export interface ShiftData {
  start_time: string;  // e.g., "11:30"
  end_time: string;    // e.g., "14:30"
  meals: number;
}

export interface DaySchedule {
  afternoon: ShiftData;
  evening: ShiftData;
}

export interface EmployeeWeekSchedule {
  name: string;
  monday: DaySchedule;
  tuesday: DaySchedule;
  wednesday: DaySchedule;
  thursday: DaySchedule;
  friday: DaySchedule;
  saturday: DaySchedule;
  sunday: DaySchedule;
}

export interface WeekPlanning {
  week_number: number;
  year: number;
  employees: EmployeeWeekSchedule[];
}

export interface PlanningResponse {
  success: boolean;
  message: string;
  data: WeekPlanning | null;
}

export interface ChatMessage {
  message: string;
  planning_id?: string;
}

export interface ChatResponse {
  response: string;
  planning_updated: boolean;
  planning: WeekPlanning | null;
}

export interface UploadResponse {
  success: boolean;
  message: string;
  file_id: string;
  filename: string;
}

export type HistoryEntryType = 'import_pdf' | 'import_excel' | 'export_pdf' | 'export_excel';

export interface HistoryEntry {
  id: string;
  type: HistoryEntryType;
  filename: string;
  timestamp: string;
  week_number?: number;
  year?: number;
}

export interface HistoryResponse {
  success: boolean;
  entries: HistoryEntry[];
}

export type DayOfWeek = 'monday' | 'tuesday' | 'wednesday' | 'thursday' | 'friday' | 'saturday' | 'sunday';

// Utility functions
export function getTimeRange(shift: ShiftData): string {
  if (shift.start_time && shift.end_time) {
    return `${shift.start_time} - ${shift.end_time}`;
  }
  return '';
}

export function getShiftHours(shift: ShiftData): number {
  if (!shift.start_time || !shift.end_time) return 0;
  try {
    const [startH, startM] = shift.start_time.split(':').map(Number);
    const [endH, endM] = shift.end_time.split(':').map(Number);
    const startMinutes = startH * 60 + startM;
    let endMinutes = endH * 60 + endM;
    // Handle shifts that cross midnight (e.g., 17:30 - 00:00)
    if (endMinutes < startMinutes) {
      endMinutes += 24 * 60; // Add 24 hours
    }
    return (endMinutes - startMinutes) / 60;
  } catch {
    return 0;
  }
}

export function getDayHours(day: DaySchedule): number {
  return getShiftHours(day.afternoon) + getShiftHours(day.evening);
}

export function getDayMeals(day: DaySchedule): number {
  return day.afternoon.meals + day.evening.meals;
}

export function getWeekDates(weekNumber: number, year: number): { start: string; end: string } {
  // Trouver le premier jour de l'année
  const jan1 = new Date(year, 0, 1);
  const dayOfWeek = jan1.getDay();

  // Calculer le premier lundi de l'année (semaine ISO)
  let firstMonday: Date;
  if (dayOfWeek <= 4) {
    // Si jan1 est lun-jeu, le premier lundi est dans la même semaine ou avant
    firstMonday = new Date(year, 0, 1 - ((dayOfWeek + 6) % 7));
  } else {
    // Si jan1 est ven-dim, le premier lundi est la semaine suivante
    firstMonday = new Date(year, 0, 1 + (8 - dayOfWeek));
  }

  // Calculer le lundi de la semaine demandée
  const targetMonday = new Date(firstMonday);
  targetMonday.setDate(firstMonday.getDate() + (weekNumber - 1) * 7);

  const targetSunday = new Date(targetMonday);
  targetSunday.setDate(targetMonday.getDate() + 6);

  const formatDate = (date: Date): string => {
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  };

  return {
    start: formatDate(targetMonday),
    end: formatDate(targetSunday),
  };
}
