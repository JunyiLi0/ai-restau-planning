from datetime import datetime
import uuid

from fastapi import APIRouter, HTTPException, Depends, Body

from app.core.config import settings
from app.api.deps import PlanningStore, get_planning_store
from app.models.schemas import WeekPlanning, PlanningResponse, AIUpdateRequest
from app.services.excel_handler import excel_handler
from app.services.ai_planner import ai_planner

router = APIRouter()


@router.get("/current", response_model=PlanningResponse)
async def get_current_planning(
    store: PlanningStore = Depends(get_planning_store),
):
    if store.current_planning is None:
        return PlanningResponse(
            success=False,
            message="No planning loaded. Upload a file or generate a new planning.",
            data=None,
        )

    return PlanningResponse(
        success=True,
        message="Current planning retrieved",
        data=store.current_planning,
    )


@router.put("/update", response_model=PlanningResponse)
async def update_planning(
    planning: WeekPlanning,
    store: PlanningStore = Depends(get_planning_store),
):
    store.current_planning = planning

    # Update Excel file if one exists
    if store.planning_file:
        excel_handler.update_planning_in_excel(store.planning_file, planning)

    return PlanningResponse(
        success=True,
        message="Planning updated successfully",
        data=planning,
    )


@router.post("/generate", response_model=PlanningResponse)
async def generate_planning(
    instructions: str = Body(..., embed=True),
    week_number: int = Body(default=None),
    year: int = Body(default=None),
    store: PlanningStore = Depends(get_planning_store),
):
    # Use current week/year if not specified
    now = datetime.now()
    if week_number is None:
        week_number = now.isocalendar()[1]
    if year is None:
        year = now.year

    try:
        planning = ai_planner.generate_planning(
            instructions=instructions,
            week_number=week_number,
            year=year,
        )

        store.current_planning = planning

        # Save as Excel
        file_id = str(uuid.uuid4())
        excel_path = settings.template_path / f"planning_{file_id}.xlsx"
        wb = excel_handler.create_planning_workbook(planning)
        excel_handler.save_workbook(wb, excel_path)
        store.planning_file = excel_path

        return PlanningResponse(
            success=True,
            message="Planning generated successfully",
            data=planning,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating planning: {str(e)}")


@router.put("/ai-update", response_model=PlanningResponse)
async def ai_update_planning(
    request: AIUpdateRequest,
    store: PlanningStore = Depends(get_planning_store),
):
    if store.current_planning is None:
        raise HTTPException(
            status_code=400,
            detail="No planning loaded. Upload an Excel file or generate a planning first.",
        )

    try:
        updated_planning = ai_planner.update_planning(
            current_planning=store.current_planning,
            instructions=request.instructions,
        )

        store.current_planning = updated_planning

        # Update Excel file if one exists
        if store.planning_file:
            excel_handler.update_planning_in_excel(store.planning_file, updated_planning)

        return PlanningResponse(
            success=True,
            message="Planning updated with AI successfully",
            data=updated_planning,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating planning: {str(e)}")


@router.delete("/clear", response_model=PlanningResponse)
async def clear_planning(
    store: PlanningStore = Depends(get_planning_store),
):
    store.clear()

    return PlanningResponse(
        success=True,
        message="Planning cleared successfully",
        data=None,
    )
