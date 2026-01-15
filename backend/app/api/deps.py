from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid

from app.core.config import settings
from app.models.schemas import WeekPlanning, HistoryEntry, HistoryEntryType


# In-memory storage for current session
# In production, this would be a database
class PlanningStore:
    def __init__(self):
        self._current_planning: Optional[WeekPlanning] = None
        self._planning_file: Optional[Path] = None
        self._uploaded_files: dict[str, Path] = {}
        self._history: list[HistoryEntry] = []

    @property
    def current_planning(self) -> Optional[WeekPlanning]:
        return self._current_planning

    @current_planning.setter
    def current_planning(self, value: WeekPlanning):
        self._current_planning = value

    @property
    def planning_file(self) -> Optional[Path]:
        return self._planning_file

    @planning_file.setter
    def planning_file(self, value: Path):
        self._planning_file = value

    @property
    def history(self) -> list[HistoryEntry]:
        return self._history

    def add_uploaded_file(self, file_path: Path) -> str:
        file_id = str(uuid.uuid4())
        self._uploaded_files[file_id] = file_path
        return file_id

    def get_uploaded_file(self, file_id: str) -> Optional[Path]:
        return self._uploaded_files.get(file_id)

    def add_history_entry(
        self,
        entry_type: HistoryEntryType,
        filename: str,
        week_number: Optional[int] = None,
        year: Optional[int] = None,
    ) -> HistoryEntry:
        entry = HistoryEntry(
            id=str(uuid.uuid4()),
            type=entry_type,
            filename=filename,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            week_number=week_number,
            year=year,
        )
        self._history.insert(0, entry)  # Most recent first
        return entry

    def clear(self):
        self._current_planning = None
        self._planning_file = None
        self._uploaded_files.clear()
        # Ne pas effacer l'historique lors du clear


planning_store = PlanningStore()


def get_planning_store() -> PlanningStore:
    return planning_store
