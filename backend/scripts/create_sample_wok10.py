#!/usr/bin/env python3
"""Script to create sample WOK10 Excel planning file with real data."""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.models.schemas import WeekPlanning, EmployeeWeekSchedule, DaySchedule, ShiftData
from app.services.excel_handler import excel_handler


def parse_time(time_str: str) -> tuple[str, str]:
    """Parse time string like '10H30-15H30' or '10h30-15h00' into (start, end)."""
    if not time_str or time_str == "-":
        return "", ""
    # Normalize format
    time_str = time_str.upper().replace("H", ":")
    parts = time_str.split("-")
    if len(parts) == 2:
        start = parts[0].strip()
        end = parts[1].strip()
        # Ensure format is HH:MM
        if len(start) == 4:  # e.g., "10:30" -> OK, "8:30" needs padding
            start = start
        return start, end
    return "", ""


def create_employee(name: str, schedule_data: list) -> EmployeeWeekSchedule:
    """Create employee with schedule data.
    schedule_data is a list of tuples: [(midi, soir), ...] for each day
    """
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    employee = EmployeeWeekSchedule(name=name)

    for i, day in enumerate(days):
        if i < len(schedule_data):
            midi, soir = schedule_data[i]
            midi_start, midi_end = parse_time(midi)
            soir_start, soir_end = parse_time(soir)

            # Repas = 1 si travail, 0 sinon
            midi_meals = 1 if midi_start else 0
            soir_meals = 1 if soir_start else 0

            day_schedule = DaySchedule(
                afternoon=ShiftData(start_time=midi_start, end_time=midi_end, meals=midi_meals),
                evening=ShiftData(start_time=soir_start, end_time=soir_end, meals=soir_meals),
            )
            setattr(employee, day, day_schedule)

    return employee


def create_wok10_planning() -> WeekPlanning:
    """Create WOK10 planning data from the image."""
    employees = [
        create_employee("THIRUCHELVAM Kovin", [
            ("-", "-"),  # Lundi
            ("-", "-"),  # Mardi
            ("-", "-"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("-", "17:30-23:00"),  # Vendredi
            ("10:30-15:00", "17:30-23:00"),  # Samedi
            ("10:30-18:00", "-"),  # Dimanche
        ]),
        create_employee("DACKO David", [
            ("10:30-15:30", "-"),  # Lundi
            ("-", "10:30-15:30"),  # Mardi
            ("10:30-15:00", "-"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("-", "-"),  # Vendredi
            ("-", "17:30-00:00"),  # Samedi
            ("-", "-"),  # Dimanche
        ]),
        create_employee("FATY Kalilou", [
            ("10:30-14:30", "18:00-23:00"),  # Lundi
            ("-", "-"),  # Mardi
            ("10:30-15:00", "18:00-23:00"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("10:30-15:00", "18:00-23:00"),  # Vendredi
            ("10:30-15:00", "18:00-23:00"),  # Samedi
            ("-", "-"),  # Dimanche
        ]),
        create_employee("LI Hai", [
            ("10:00-14:30", "17:30-22:30"),  # Lundi
            ("10:00-14:30", "17:30-22:30"),  # Mardi
            ("10:00-14:30", "17:30-22:30"),  # Mercredi
            ("10:00-14:30", "-"),  # Jeudi
            ("-", "-"),  # Vendredi
            ("-", "-"),  # Samedi
            ("10:00-14:30", "-"),  # Dimanche
        ]),
        create_employee("LI Huiha", [
            ("10:30-15:00", "17:30-23:00"),  # Lundi
            ("10:30-15:00", "17:30-23:00"),  # Mardi
            ("10:30-15:00", "17:30-23:00"),  # Mercredi
            ("10:30-15:00", "17:30-23:00"),  # Jeudi
            ("10:30-15:00", "-"),  # Vendredi
            ("10:30-15:00", "18:00-00:00"),  # Samedi
            ("10:30-15:00", "-"),  # Dimanche
        ]),
        create_employee("WANG Lisa", [
            ("10:30-15:00", "18:00-23:00"),  # Lundi
            ("10:30-15:00", "18:00-23:00"),  # Mardi
            ("10:30-15:00", "18:00-23:00"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("10:30-15:00", "-"),  # Vendredi
            ("10:30-15:00", "18:00-00:00"),  # Samedi
            ("10:30-15:00", "-"),  # Dimanche
        ]),
        create_employee("LI Lifen", [
            ("-", "-"),  # Lundi
            ("-", "-"),  # Mardi
            ("10:30-15:00", "18:00-23:00"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("10:30-17:00", "-"),  # Vendredi
            ("10:30-17:00", "-"),  # Samedi
            ("-", "-"),  # Dimanche
        ]),
        create_employee("MAHESWARAN Raniammah", [
            ("-", "-"),  # Lundi
            ("10:30-16:00", "-"),  # Mardi
            ("-", "-"),  # Mercredi
            ("10:30-17:00", "-"),  # Jeudi
            ("10:30-17:00", "-"),  # Vendredi
            ("10:30-17:00", "-"),  # Samedi
            ("-", "-"),  # Dimanche
        ]),
        create_employee("ABEGA MENYENG Joseph", [
            ("10:30-15:00", "-"),  # Lundi
            ("10:30-15:00", "17:30-23:00"),  # Mardi
            ("10:30-15:00", "17:30-23:00"),  # Mercredi
            ("10:30-15:00", "17:30-23:00"),  # Jeudi
            ("10:30-15:00", "17:30-23:00"),  # Vendredi
            ("10:30-15:00", "17:30-23:00"),  # Samedi
            ("17:30-23:00", "-"),  # Dimanche
        ]),
        create_employee("WANG Liuyun", [
            ("-", "-"),  # Lundi
            ("-", "-"),  # Mardi
            ("10:30-15:00", "17:30-23:00"),  # Mercredi
            ("10:30-15:00", "17:30-23:00"),  # Jeudi
            ("10:00-14:30", "17:30-23:00"),  # Vendredi
            ("10:00-14:30", "-"),  # Samedi
            ("10:00-14:30", "17:30-22:30"),  # Dimanche
        ]),
        create_employee("NI Aiying", [
            ("10:00-14:30", "-"),  # Lundi
            ("-", "-"),  # Mardi
            ("-", "-"),  # Mercredi
            ("10:00-14:30", "-"),  # Jeudi
            ("10:30-15:00", "-"),  # Vendredi
            ("10:30-15:00", "17:00-00:00"),  # Samedi
            ("-", "17:30-23:00"),  # Dimanche
        ]),
        create_employee("PEJA Naima", [
            ("10:30-15:00", "-"),  # Lundi
            ("-", "-"),  # Mardi
            ("10:30-15:00", "-"),  # Mercredi
            ("10:30-15:00", "-"),  # Jeudi
            ("18:00-23:00", "-"),  # Vendredi
            ("10:30-15:00", "17:00-00:00"),  # Samedi
            ("-", "17:30-23:00"),  # Dimanche
        ]),
        create_employee("SONAM Dolma", [
            ("-", "-"),  # Lundi
            ("-", "-"),  # Mardi
            ("-", "10:00-18:30"),  # Mercredi
            ("10:30-15:00", "-"),  # Jeudi
            ("18:00-23:00", "-"),  # Vendredi
            ("18:00-23:00", "-"),  # Samedi
            ("10:30-20:30", "-"),  # Dimanche
        ]),
        create_employee("TENZIN Sangpo", [
            ("-", "-"),  # Lundi
            ("10:00-15:30", "18:30-21:00"),  # Mardi
            ("10:00-15:00", "18:30-21:00"),  # Mercredi
            ("10:00-15:00", "18:30-21:00"),  # Jeudi
            ("10:00-15:00", "18:30-21:00"),  # Vendredi
            ("10:30-15:00", "-"),  # Samedi
            ("17:30-23:00", "-"),  # Dimanche
        ]),
        create_employee("THIRUCHELVAM Pravin", [
            ("-", "-"),  # Lundi
            ("-", "-"),  # Mardi
            ("-", "-"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("-", "17:30-23:00"),  # Vendredi
            ("17:30-23:00", "-"),  # Samedi
            ("10:30-15:00", "-"),  # Dimanche
        ]),
        create_employee("THIRUCHELVAM Logika", [
            ("-", "-"),  # Lundi
            ("-", "-"),  # Mardi
            ("-", "-"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("-", "-"),  # Vendredi
            ("-", "18:30-21:00"),  # Samedi
            ("-", "-"),  # Dimanche
        ]),
        create_employee("THIRUCHELVAM Poobalapillai", [
            ("08:00-10:00", "15:30-17:30"),  # Lundi
            ("08:00-10:00", "15:30-17:00"),  # Mardi
            ("08:00-10:00", "15:30-17:30"),  # Mercredi
            ("08:00-10:00", "15:30-17:30"),  # Jeudi
            ("08:00-10:00", "15:30-17:30"),  # Vendredi
            ("08:00-10:00", "15:30-17:30"),  # Samedi
            ("-", "-"),  # Dimanche
        ]),
        create_employee("Mme TENZIN Pema", [
            ("-", "-"),  # Lundi
            ("17:30-22:30", "10:00-14:30"),  # Mardi
            ("-", "-"),  # Mercredi
            ("-", "10:00-14:30"),  # Jeudi
            ("17:30-22:30", "10:00-14:30"),  # Vendredi
            ("17:30-23:00", "-"),  # Samedi
            ("10:00-14:30", "17:30-22:30"),  # Dimanche
        ]),
        create_employee("TOGOLA Demba", [
            ("-", "-"),  # Lundi
            ("10:30-15:00", "18:00-23:00"),  # Mardi
            ("-", "18:00-23:00"),  # Mercredi
            ("10:30-15:00", "-"),  # Jeudi
            ("10:30-15:00", "18:00-23:00"),  # Vendredi
            ("10:30-15:00", "18:00-00:00"),  # Samedi
            ("10:30-15:00", "-"),  # Dimanche
        ]),
        create_employee("XU Zhihai", [
            ("10:00-14:30", "17:30-22:30"),  # Lundi
            ("10:00-14:30", "-"),  # Mardi
            ("10:00-14:30", "17:30-22:30"),  # Mercredi
            ("10:00-14:30", "17:30-22:30"),  # Jeudi
            ("-", "-"),  # Vendredi
            ("-", "-"),  # Samedi
            ("-", "17:30-23:00"),  # Dimanche
        ]),
        create_employee("M KUNDER NAIMA", [
            ("-", "-"),  # Lundi
            ("10:30-15:30", "18:30-21:00"),  # Mardi
            ("10:00-15:30", "18:30-21:00"),  # Mercredi
            ("10:00-15:30", "18:30-21:00"),  # Jeudi
            ("10:00-15:30", "18:30-21:00"),  # Vendredi
            ("10:30-15:00", "18:30-21:00"),  # Samedi
            ("-", "10:30-15:00"),  # Dimanche
        ]),
        create_employee("XU Huanbin", [
            ("-", "-"),  # Lundi
            ("10:30-15:00", "18:00-23:00"),  # Mardi
            ("10:30-15:00", "-"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("10:30-15:00", "18:00-23:00"),  # Vendredi
            ("10:30-15:00", "18:00-00:00"),  # Samedi
            ("-", "-"),  # Dimanche
        ]),
        create_employee("SHEN Qinqin", [
            ("10:30-14:30", "17:30-22:30"),  # Lundi
            ("-", "17:30-23:00"),  # Mardi
            ("10:30-14:30", "17:30-22:30"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("-", "-"),  # Vendredi
            ("10:30-15:30", "18:30-23:30"),  # Samedi
            ("-", "-"),  # Dimanche
        ]),
        create_employee("XU Jianying", [
            ("10:30-15:00", "17:30-23:00"),  # Lundi
            ("10:30-15:00", "17:30-23:00"),  # Mardi
            ("10:30-15:00", "17:30-23:00"),  # Mercredi
            ("-", "-"),  # Jeudi
            ("-", "-"),  # Vendredi
            ("10:30-14:30", "-"),  # Samedi
            ("-", "17:30-23:00"),  # Dimanche
        ]),
    ]

    return WeekPlanning(
        week_number=3,
        year=2025,
        employees=employees
    )


def main():
    # Create WOK10 planning
    planning = create_wok10_planning()

    # Create workbook
    wb = excel_handler.create_planning_workbook(planning)

    # Save to templates directory
    output_path = Path(__file__).parent.parent / "data" / "templates" / "sample_planning_wok10.xlsx"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    excel_handler.save_workbook(wb, output_path)
    print(f"Sample WOK10 Excel file created: {output_path}")

    # Print summary
    print(f"\nNombre d'employés: {len(planning.employees)}")
    print("\nEmployés:")
    for emp in planning.employees:
        print(f"  - {emp.name}: {emp.weekly_hours:.1f}h/semaine, {emp.weekly_meals} repas")


if __name__ == "__main__":
    main()
