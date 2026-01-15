from pydantic import BaseModel
from typing import Optional
from enum import Enum


class DayOfWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class ShiftData(BaseModel):
    start_time: str = ""  # e.g., "11:30"
    end_time: str = ""    # e.g., "14:30"
    meals: int = 0

    @property
    def hours(self) -> float:
        """Calculate hours from time range."""
        if not self.start_time or not self.end_time:
            return 0.0
        try:
            start_h, start_m = map(int, self.start_time.split(":"))
            end_h, end_m = map(int, self.end_time.split(":"))
            start_minutes = start_h * 60 + start_m
            end_minutes = end_h * 60 + end_m
            return (end_minutes - start_minutes) / 60
        except (ValueError, AttributeError):
            return 0.0

    @property
    def time_range(self) -> str:
        """Return formatted time range or empty string."""
        if self.start_time and self.end_time:
            return f"{self.start_time} - {self.end_time}"
        return ""


class DaySchedule(BaseModel):
    afternoon: ShiftData = ShiftData()
    evening: ShiftData = ShiftData()

    @property
    def total_hours(self) -> float:
        return self.afternoon.hours + self.evening.hours

    @property
    def total_meals(self) -> int:
        return self.afternoon.meals + self.evening.meals


class EmployeeWeekSchedule(BaseModel):
    name: str
    monday: DaySchedule = DaySchedule()
    tuesday: DaySchedule = DaySchedule()
    wednesday: DaySchedule = DaySchedule()
    thursday: DaySchedule = DaySchedule()
    friday: DaySchedule = DaySchedule()
    saturday: DaySchedule = DaySchedule()
    sunday: DaySchedule = DaySchedule()

    @property
    def weekly_hours(self) -> float:
        return sum(
            getattr(self, day).total_hours
            for day in [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]
        )

    @property
    def weekly_meals(self) -> int:
        return sum(
            getattr(self, day).total_meals
            for day in [
                "monday",
                "tuesday",
                "wednesday",
                "thursday",
                "friday",
                "saturday",
                "sunday",
            ]
        )


class WeekPlanning(BaseModel):
    week_number: int
    year: int
    employees: list[EmployeeWeekSchedule] = []


class PlanningResponse(BaseModel):
    success: bool
    message: str
    data: Optional[WeekPlanning] = None


class ChatMessage(BaseModel):
    message: str
    planning_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    planning_updated: bool = False
    planning: Optional[WeekPlanning] = None


class AIUpdateRequest(BaseModel):
    instructions: str
    planning_id: Optional[str] = None


class UploadResponse(BaseModel):
    success: bool
    message: str
    file_id: str
    filename: str


class HistoryEntryType(str, Enum):
    IMPORT_PDF = "import_pdf"
    IMPORT_EXCEL = "import_excel"
    EXPORT_PDF = "export_pdf"
    EXPORT_EXCEL = "export_excel"


class HistoryEntry(BaseModel):
    id: str
    type: HistoryEntryType
    filename: str
    timestamp: str
    week_number: Optional[int] = None
    year: Optional[int] = None


class HistoryResponse(BaseModel):
    success: bool
    entries: list[HistoryEntry] = []
