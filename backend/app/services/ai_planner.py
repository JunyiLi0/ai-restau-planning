import json
from typing import Optional

from app.core.ai_client import get_openai_client
from app.models.schemas import WeekPlanning, EmployeeWeekSchedule, DaySchedule, ShiftData


SYSTEM_PROMPT = """Tu es un assistant IA spécialisé dans la planification des horaires des employés de restaurant.
Tu aides à créer et modifier les plannings hebdomadaires du personnel.

Règles pour les horaires:
- Chaque jour a deux services: midi (afternoon) et soir (evening)
- Pour chaque service, tu dois spécifier: start_time, end_time (format "HH:MM"), et meals (nombre de repas)
- Service midi typique: 10:30-15:00
- Service soir typique: 17:30-23:00 (peut aller jusqu'à 00:00 pour les samedis)
- Si un employé ne travaille pas un service, utiliser start_time: null et end_time: null
- Chaque employé qui travaille un service a droit à 1 repas par service

Réponds TOUJOURS avec du JSON valide dans ce format exact:
{
    "week_number": <int>,
    "year": <int>,
    "employees": [
        {
            "name": "NOM Prénom",
            "monday": {
                "afternoon": {"start_time": "10:30", "end_time": "15:00", "meals": 1},
                "evening": {"start_time": "17:30", "end_time": "23:00", "meals": 1}
            },
            "tuesday": {
                "afternoon": {"start_time": null, "end_time": null, "meals": 0},
                "evening": {"start_time": "18:00", "end_time": "23:00", "meals": 1}
            },
            ... (pour chaque jour de la semaine: monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        }
    ]
}

Notes importantes:
- Les heures doivent être au format "HH:MM" (ex: "10:30", "17:30", "00:00")
- Si pas de travail sur un service: start_time: null, end_time: null, meals: 0
- meals = 1 si l'employé travaille le service, 0 sinon
- Les noms doivent être au format "NOM Prénom" (ex: "DUPONT Jean")
"""


class AIPlanner:
    def __init__(self):
        self.client = None

    def _get_client(self):
        if self.client is None:
            self.client = get_openai_client()
        return self.client

    def generate_planning(
        self,
        instructions: str,
        week_number: int = 1,
        year: int = 2024,
    ) -> WeekPlanning:
        client = self._get_client()

        user_prompt = f"""Crée un planning hebdomadaire des employés pour la semaine {week_number} de {year}.

Instructions de l'utilisateur:
{instructions}

Génère le planning au format JSON avec les plages horaires (start_time, end_time)."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        return self._parse_response(response.choices[0].message.content)

    def update_planning(
        self,
        current_planning: WeekPlanning,
        instructions: str,
    ) -> WeekPlanning:
        client = self._get_client()

        current_json = current_planning.model_dump_json(indent=2)

        user_prompt = f"""Voici le planning actuel des employés:
{current_json}

Modifie ce planning selon ces instructions:
{instructions}

Retourne le planning complet mis à jour au format JSON."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        return self._parse_response(response.choices[0].message.content)

    def process_chat_message(
        self,
        message: str,
        current_planning: Optional[WeekPlanning] = None,
    ) -> tuple[str, Optional[WeekPlanning]]:
        client = self._get_client()

        context = ""
        if current_planning:
            context = f"\n\nCurrent schedule:\n{current_planning.model_dump_json(indent=2)}"

        user_prompt = f"""Message de l'utilisateur: {message}{context}

Si l'utilisateur demande de créer ou modifier un planning, réponds avec le planning JSON.
Si l'utilisateur pose une question, réponds de manière conversationnelle mais inclus les modifications de planning en JSON si applicable.

Si tu fournis un planning, assure-toi de l'inclure en JSON valide dans un bloc ```json```."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
        )

        response_text = response.choices[0].message.content

        # Try to extract JSON from response
        planning = None
        if "```json" in response_text:
            try:
                json_str = response_text.split("```json")[1].split("```")[0].strip()
                planning = self._parse_response(json_str)
            except (IndexError, json.JSONDecodeError):
                pass

        return response_text, planning

    def process_pdf_content(
        self,
        pdf_text: str,
        pdf_tables: list,
        additional_instructions: str = "",
    ) -> WeekPlanning:
        client = self._get_client()

        tables_str = json.dumps(pdf_tables, indent=2) if pdf_tables else "No tables found"

        user_prompt = f"""Extrais les informations de planning des employés du contenu PDF suivant et crée un planning hebdomadaire.

Texte du PDF:
{pdf_text}

Tableaux du PDF:
{tables_str}

{f'Instructions supplémentaires: {additional_instructions}' if additional_instructions else ''}

Crée un planning complet basé sur ces informations. Si des données manquent, fais des hypothèses raisonnables pour un planning de restaurant."""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        return self._parse_response(response.choices[0].message.content)

    def _parse_response(self, response_text: str) -> WeekPlanning:
        data = json.loads(response_text)

        employees = []
        for emp_data in data.get("employees", []):
            emp = EmployeeWeekSchedule(name=emp_data["name"])

            for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                if day in emp_data:
                    day_data = emp_data[day]
                    afternoon_data = day_data.get("afternoon", {})
                    evening_data = day_data.get("evening", {})

                    day_schedule = DaySchedule(
                        afternoon=ShiftData(
                            start_time=afternoon_data.get("start_time") or "",
                            end_time=afternoon_data.get("end_time") or "",
                            meals=int(afternoon_data.get("meals", 0)),
                        ),
                        evening=ShiftData(
                            start_time=evening_data.get("start_time") or "",
                            end_time=evening_data.get("end_time") or "",
                            meals=int(evening_data.get("meals", 0)),
                        ),
                    )
                    setattr(emp, day, day_schedule)

            employees.append(emp)

        return WeekPlanning(
            week_number=data.get("week_number", 1),
            year=data.get("year", 2024),
            employees=employees,
        )


ai_planner = AIPlanner()
