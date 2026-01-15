import uuid
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from app.core.config import settings
from app.api.deps import PlanningStore, get_planning_store
from app.models.schemas import HistoryEntryType
from app.services.pdf_generator import pdf_generator
from app.services.excel_handler import excel_handler

router = APIRouter()


@router.get("/pdf")
async def export_pdf(
    store: PlanningStore = Depends(get_planning_store),
):
    if store.current_planning is None:
        raise HTTPException(
            status_code=400,
            detail="No planning loaded. Upload a file or generate a planning first.",
        )

    try:
        file_id = str(uuid.uuid4())
        pdf_path = settings.export_path / f"planning_{file_id}.pdf"

        pdf_generator.generate_planning_pdf(store.current_planning, pdf_path)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"planning_semaine{store.current_planning.week_number}_{store.current_planning.year}_{timestamp}.pdf"

        # Add history entry
        store.add_history_entry(
            entry_type=HistoryEntryType.EXPORT_PDF,
            filename=filename,
            week_number=store.current_planning.week_number,
            year=store.current_planning.year,
        )

        return FileResponse(
            path=pdf_path,
            filename=filename,
            media_type="application/pdf",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")


@router.get("/excel")
async def export_excel(
    store: PlanningStore = Depends(get_planning_store),
):
    if store.current_planning is None:
        raise HTTPException(
            status_code=400,
            detail="No planning loaded. Upload a file or generate a planning first.",
        )

    try:
        file_id = str(uuid.uuid4())
        excel_path = settings.export_path / f"planning_{file_id}.xlsx"

        wb = excel_handler.create_planning_workbook(store.current_planning)
        excel_handler.save_workbook(wb, excel_path)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"planning_semaine{store.current_planning.week_number}_{store.current_planning.year}_{timestamp}.xlsx"

        # Add history entry
        store.add_history_entry(
            entry_type=HistoryEntryType.EXPORT_EXCEL,
            filename=filename,
            week_number=store.current_planning.week_number,
            year=store.current_planning.year,
        )

        return FileResponse(
            path=excel_path,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Excel: {str(e)}")
