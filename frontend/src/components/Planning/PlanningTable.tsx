import React from 'react';
import type { WeekPlanning, DayOfWeek } from '../../types';
import { getTimeRange, getShiftHours } from '../../types';

interface PlanningTableProps {
  planning: WeekPlanning;
}

const DAYS: DayOfWeek[] = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'];
const DAY_LABELS_FR = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim'];

export function PlanningTable({ planning }: PlanningTableProps) {
  const getTotalHours = (employeeIndex: number) => {
    const employee = planning.employees[employeeIndex];
    return DAYS.reduce((sum, day) => {
      return sum + getShiftHours(employee[day].afternoon) + getShiftHours(employee[day].evening);
    }, 0);
  };

  const getTotalMeals = (employeeIndex: number) => {
    const employee = planning.employees[employeeIndex];
    return DAYS.reduce((sum, day) => {
      return sum + employee[day].afternoon.meals + employee[day].evening.meals;
    }, 0);
  };


  return (
    <div className="overflow-x-auto">
      <table className="min-w-full border-collapse text-sm">
        <thead>
          <tr className="bg-blue-600 text-white">
            <th className="border border-blue-700 px-2 py-2" rowSpan={2}>
              Employé
            </th>
            {DAY_LABELS_FR.map((day) => (
              <th key={day} className="border border-blue-700 px-2 py-1" colSpan={4}>
                {day}
              </th>
            ))}
            <th className="border border-blue-700 px-2 py-1" colSpan={2}>
              Total
            </th>
          </tr>
          <tr className="bg-blue-100 text-gray-800">
            {DAYS.map((day) => (
              <React.Fragment key={day}>
                <th className="border border-gray-300 px-1 py-1 text-xs">
                  Midi
                </th>
                <th className="border border-gray-300 px-1 py-1 text-xs">
                  Repas
                </th>
                <th className="border border-gray-300 px-1 py-1 text-xs">
                  Soir
                </th>
                <th className="border border-gray-300 px-1 py-1 text-xs">
                  Repas
                </th>
              </React.Fragment>
            ))}
            <th className="border border-gray-300 px-1 py-1 text-xs">Heures</th>
            <th className="border border-gray-300 px-1 py-1 text-xs">Repas</th>
          </tr>
        </thead>
        <tbody>
          {planning.employees.map((employee, idx) => (
            <tr key={employee.name} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
              <td className="border border-gray-300 px-2 py-1 font-medium">
                {employee.name}
              </td>
              {DAYS.map((day) => (
                <React.Fragment key={`${employee.name}-${day}`}>
                  <td className="border border-gray-300 px-1 py-1 text-center text-xs whitespace-nowrap">
                    {getTimeRange(employee[day].afternoon) || '-'}
                  </td>
                  <td className="border border-gray-300 px-1 py-1 text-center">
                    {employee[day].afternoon.meals || '-'}
                  </td>
                  <td className="border border-gray-300 px-1 py-1 text-center text-xs whitespace-nowrap">
                    {getTimeRange(employee[day].evening) || '-'}
                  </td>
                  <td className="border border-gray-300 px-1 py-1 text-center">
                    {employee[day].evening.meals || '-'}
                  </td>
                </React.Fragment>
              ))}
              <td className="border border-gray-300 px-1 py-1 text-center font-medium">
                {getTotalHours(idx).toFixed(1)}
              </td>
              <td className="border border-gray-300 px-1 py-1 text-center font-medium">
                {getTotalMeals(idx)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
