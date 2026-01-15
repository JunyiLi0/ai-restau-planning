from pathlib import Path
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak

from app.models.schemas import WeekPlanning, EmployeeWeekSchedule


# Première ligne : Lundi à Jeudi
DAYS_ROW1 = ["monday", "tuesday", "wednesday", "thursday"]
DAY_LABELS_ROW1 = ["Lundi", "Mardi", "Mercredi", "Jeudi"]

# Deuxième ligne : Vendredi à Dimanche
DAYS_ROW2 = ["friday", "saturday", "sunday"]
DAY_LABELS_ROW2 = ["Vendredi", "Samedi", "Dimanche"]

MAX_EMPLOYEES_PER_PAGE = 10


def get_next_week_dates() -> tuple[int, int, str, str]:
    """Retourne le numéro de semaine, l'année, et les dates de la semaine prochaine."""
    today = datetime.now()
    # Trouver le lundi de la semaine prochaine
    days_until_monday = (7 - today.weekday()) % 7
    if days_until_monday == 0:
        days_until_monday = 7  # Si on est lundi, prendre le lundi suivant
    next_monday = today + timedelta(days=days_until_monday)
    next_sunday = next_monday + timedelta(days=6)

    week_number = next_monday.isocalendar()[1]
    year = next_monday.year

    start_date = next_monday.strftime("%d/%m/%Y")
    end_date = next_sunday.strftime("%d/%m/%Y")

    return week_number, year, start_date, end_date


class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            "CustomTitle",
            parent=self.styles["Heading1"],
            fontSize=14,
            spaceAfter=20,
            alignment=1,  # Center
        )

    def generate_planning_pdf(self, planning: WeekPlanning, output_path: Path) -> Path:
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=landscape(A4),
            rightMargin=1 * cm,
            leftMargin=1 * cm,
            topMargin=1 * cm,
            bottomMargin=1 * cm,
        )

        elements = []

        # Calculer les dates de la semaine prochaine
        week_num, year, start_date, end_date = get_next_week_dates()

        # Utiliser les valeurs du planning si disponibles, sinon semaine prochaine
        if planning.week_number and planning.year:
            week_num = planning.week_number
            year = planning.year
            # Recalculer les dates pour cette semaine spécifique
            start_date, end_date = self._get_week_dates(week_num, year)

        # Diviser les employés en groupes de MAX_EMPLOYEES_PER_PAGE
        employee_groups = self._split_employees(planning.employees, MAX_EMPLOYEES_PER_PAGE)

        for group_idx, employee_group in enumerate(employee_groups):
            if group_idx > 0:
                elements.append(PageBreak())

            # Titre
            title = Paragraph(
                f"Planning des employés WOK10 - Semaine {week_num} du {start_date} au {end_date}",
                self.title_style,
            )
            elements.append(title)

            # Première partie : Lundi à Jeudi
            table1_data = self._build_table_data(employee_group, DAYS_ROW1, DAY_LABELS_ROW1, include_totals=False)
            table1 = Table(table1_data, repeatRows=2)
            table1.setStyle(self._get_table_style(len(employee_group), len(DAYS_ROW1)))
            elements.append(table1)

            elements.append(Spacer(1, 0.5 * cm))

            # Deuxième partie : Vendredi à Dimanche + Totaux
            table2_data = self._build_table_data(employee_group, DAYS_ROW2, DAY_LABELS_ROW2, include_totals=True)
            table2 = Table(table2_data, repeatRows=2)
            table2.setStyle(self._get_table_style(len(employee_group), len(DAYS_ROW2), include_totals=True))
            elements.append(table2)

        # Build PDF
        doc.build(elements)
        return output_path

    def _get_week_dates(self, week_number: int, year: int) -> tuple[str, str]:
        """Calcule les dates de début et fin pour une semaine donnée."""
        # Premier jour de l'année
        jan1 = datetime(year, 1, 1)
        # Trouver le premier lundi de l'année
        days_to_monday = (7 - jan1.weekday()) % 7
        if jan1.weekday() <= 3:  # Si jan1 est lun-jeu, c'est semaine 1
            first_monday = jan1 - timedelta(days=jan1.weekday())
        else:
            first_monday = jan1 + timedelta(days=days_to_monday)

        # Calculer le lundi de la semaine demandée
        target_monday = first_monday + timedelta(weeks=week_number - 1)
        target_sunday = target_monday + timedelta(days=6)

        return target_monday.strftime("%d/%m/%Y"), target_sunday.strftime("%d/%m/%Y")

    def _split_employees(self, employees: list[EmployeeWeekSchedule], max_per_group: int) -> list[list[EmployeeWeekSchedule]]:
        """Divise la liste d'employés en groupes."""
        groups = []
        for i in range(0, len(employees), max_per_group):
            groups.append(employees[i:i + max_per_group])
        return groups if groups else [[]]

    def _build_table_data(
        self,
        employees: list[EmployeeWeekSchedule],
        days: list[str],
        day_labels: list[str],
        include_totals: bool = False
    ) -> list[list[str]]:
        # Header row 1
        header1 = ["Employé"]
        for day in day_labels:
            header1.extend([day, "", "", ""])
        if include_totals:
            header1.extend(["Total Semaine", ""])

        # Header row 2
        header2 = [""]
        for _ in day_labels:
            header2.extend(["Midi", "Repas", "Soir", "Repas"])
        if include_totals:
            header2.extend(["Heures", "Repas"])

        data = [header1, header2]

        # Employee rows
        for employee in employees:
            row = [employee.name]
            for day in days:
                day_schedule = getattr(employee, day)
                row.extend([
                    day_schedule.afternoon.time_range if day_schedule.afternoon.time_range else "-",
                    str(day_schedule.afternoon.meals) if day_schedule.afternoon.meals else "-",
                    day_schedule.evening.time_range if day_schedule.evening.time_range else "-",
                    str(day_schedule.evening.meals) if day_schedule.evening.meals else "-",
                ])
            if include_totals:
                row.extend([
                    f"{employee.weekly_hours:.1f}",
                    str(employee.weekly_meals),
                ])
            data.append(row)

        return data

    def _get_table_style(self, num_employees: int, num_days: int, include_totals: bool = False) -> TableStyle:
        style = TableStyle([
            # Header styling
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4472C4")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#D9E2F3")),
            ("FONTNAME", (0, 0), (-1, 1), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 1), 8),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            # Grid
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            # Data rows
            ("FONTNAME", (0, 2), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 2), (-1, -1), 7),
            # Alternating row colors
            ("ROWBACKGROUNDS", (0, 2), (-1, -1), [colors.white, colors.HexColor("#F2F2F2")]),
            # Employee name column
            ("ALIGN", (0, 2), (0, -1), "LEFT"),
        ])

        # Merge header cells for days
        col = 1
        for _ in range(num_days):
            style.add("SPAN", (col, 0), (col + 3, 0))
            col += 4

        # Merge total header if included
        if include_totals:
            style.add("SPAN", (col, 0), (col + 1, 0))

        return style


pdf_generator = PDFGenerator()
