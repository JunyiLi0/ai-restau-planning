#!/usr/bin/env python3
"""Script to create a sample Excel planning file."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.schemas import WeekPlanning, EmployeeWeekSchedule, DaySchedule, ShiftData
from app.services.excel_handler import excel_handler


def create_sample_planning() -> WeekPlanning:
    """Create sample planning data with time ranges."""
    employees = [
        EmployeeWeekSchedule(
            name="Jean Dupont",
            monday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="14:30", meals=1),
                evening=ShiftData(start_time="", end_time="", meals=0)
            ),
            tuesday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="14:30", meals=1),
                evening=ShiftData(start_time="18:30", end_time="22:30", meals=1)
            ),
            wednesday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="18:30", end_time="23:00", meals=1)
            ),
            thursday=DaySchedule(
                afternoon=ShiftData(start_time="11:00", end_time="14:30", meals=1),
                evening=ShiftData(start_time="18:30", end_time="22:30", meals=1)
            ),
            friday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="14:30", meals=1),
                evening=ShiftData(start_time="18:30", end_time="23:30", meals=1)
            ),
            saturday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="", end_time="", meals=0)
            ),
            sunday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="", end_time="", meals=0)
            ),
        ),
        EmployeeWeekSchedule(
            name="Marie Martin",
            monday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="18:30", end_time="22:30", meals=1)
            ),
            tuesday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="18:30", end_time="22:30", meals=1)
            ),
            wednesday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="14:30", meals=1),
                evening=ShiftData(start_time="18:30", end_time="22:30", meals=1)
            ),
            thursday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="", end_time="", meals=0)
            ),
            friday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="14:30", meals=1),
                evening=ShiftData(start_time="18:30", end_time="23:00", meals=1)
            ),
            saturday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="15:00", meals=1),
                evening=ShiftData(start_time="18:30", end_time="23:30", meals=1)
            ),
            sunday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="", end_time="", meals=0)
            ),
        ),
        EmployeeWeekSchedule(
            name="Pierre Bernard",
            monday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="14:30", meals=1),
                evening=ShiftData(start_time="18:30", end_time="22:30", meals=1)
            ),
            tuesday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="", end_time="", meals=0)
            ),
            wednesday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="", end_time="", meals=0)
            ),
            thursday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="14:30", meals=1),
                evening=ShiftData(start_time="18:30", end_time="22:30", meals=1)
            ),
            friday=DaySchedule(
                afternoon=ShiftData(start_time="", end_time="", meals=0),
                evening=ShiftData(start_time="18:30", end_time="23:00", meals=1)
            ),
            saturday=DaySchedule(
                afternoon=ShiftData(start_time="11:30", end_time="15:00", meals=1),
                evening=ShiftData(start_time="18:30", end_time="23:30", meals=1)
            ),
            sunday=DaySchedule(
                afternoon=ShiftData(start_time="12:00", end_time="15:00", meals=1),
                evening=ShiftData(start_time="18:30", end_time="22:00", meals=1)
            ),
        ),
    ]

    return WeekPlanning(
        week_number=3,
        year=2024,
        employees=employees
    )


def main():
    # Create sample planning
    planning = create_sample_planning()

    # Create workbook
    wb = excel_handler.create_planning_workbook(planning)

    # Save to templates directory
    output_path = Path(__file__).parent.parent / "data" / "templates" / "sample_planning.xlsx"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    excel_handler.save_workbook(wb, output_path)
    print(f"Sample Excel file created: {output_path}")

    # Print summary
    print("\nEmployees:")
    for emp in planning.employees:
        print(f"  - {emp.name}: {emp.weekly_hours:.1f}h/semaine, {emp.weekly_meals} repas")


if __name__ == "__main__":
    main()
