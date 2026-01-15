import json
from typing import Optional

from app.core.ai_client import get_openai_client
from app.models.schemas import WeekPlanning, EmployeeWeekSchedule, DaySchedule, ShiftData


SYSTEM_PROMPT = """You are an AI assistant specialized in restaurant employee scheduling.
You help create and modify weekly work schedules for restaurant staff.

When creating or modifying schedules, consider:
- Each day has two shifts: afternoon and evening
- For each shift, track: hours worked and meals eaten
- Typical afternoon shift: 11:00-15:00 (4 hours)
- Typical evening shift: 18:00-23:00 (5 hours)
- Employees typically get 1 meal per shift worked

Always respond with valid JSON in the following format:
{
    "week_number": <int>,
    "year": <int>,
    "employees": [
        {
            "name": "<string>",
            "monday": {"afternoon": {"hours": <float>, "meals": <int>}, "evening": {"hours": <float>, "meals": <int>}},
            "tuesday": {"afternoon": {"hours": <float>, "meals": <int>}, "evening": {"hours": <float>, "meals": <int>}},
            "wednesday": {"afternoon": {"hours": <float>, "meals": <int>}, "evening": {"hours": <float>, "meals": <int>}},
            "thursday": {"afternoon": {"hours": <float>, "meals": <int>}, "evening": {"hours": <float>, "meals": <int>}},
            "friday": {"afternoon": {"hours": <float>, "meals": <int>}, "evening": {"hours": <float>, "meals": <int>}},
            "saturday": {"afternoon": {"hours": <float>, "meals": <int>}, "evening": {"hours": <float>, "meals": <int>}},
            "sunday": {"afternoon": {"hours": <float>, "meals": <int>}, "evening": {"hours": <float>, "meals": <int>}}
        }
    ]
}
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

        user_prompt = f"""Create a weekly employee schedule for week {week_number} of {year}.

Instructions from the user:
{instructions}

Generate the schedule as JSON."""

        response = client.chat.completions.create(
            model="gpt-4.1",
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

        user_prompt = f"""Here is the current employee schedule:
{current_json}

Please modify this schedule according to these instructions:
{instructions}

Return the complete updated schedule as JSON."""

        response = client.chat.completions.create(
            model="gpt-4.1",
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

        user_prompt = f"""User message: {message}{context}

If the user is asking to create or modify a schedule, respond with the JSON schedule.
If the user is asking a question, respond conversationally but include any schedule changes as JSON if applicable.

If you're providing a schedule, make sure to include it as valid JSON wrapped in ```json``` code blocks."""

        response = client.chat.completions.create(
            model="gpt-5.2",
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

        user_prompt = f"""Extract employee scheduling information from the following PDF content and create a weekly schedule.

PDF Text:
{pdf_text}

PDF Tables:
{tables_str}

{f'Additional instructions: {additional_instructions}' if additional_instructions else ''}

Create a complete weekly schedule based on this information. If some data is missing, make reasonable assumptions for a restaurant schedule."""

        response = client.chat.completions.create(
            model="gpt-4.1",
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
                    day_schedule = DaySchedule(
                        afternoon=ShiftData(
                            hours=float(day_data.get("afternoon", {}).get("hours", 0)),
                            meals=int(day_data.get("afternoon", {}).get("meals", 0)),
                        ),
                        evening=ShiftData(
                            hours=float(day_data.get("evening", {}).get("hours", 0)),
                            meals=int(day_data.get("evening", {}).get("meals", 0)),
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
