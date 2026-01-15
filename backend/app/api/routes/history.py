from fastapi import APIRouter, Depends

from app.api.deps import PlanningStore, get_planning_store
from app.models.schemas import HistoryResponse

router = APIRouter()


@router.get("/", response_model=HistoryResponse)
async def get_history(
    store: PlanningStore = Depends(get_planning_store),
):
    """Get the history of imports and exports."""
    return HistoryResponse(
        success=True,
        entries=store.history,
    )
