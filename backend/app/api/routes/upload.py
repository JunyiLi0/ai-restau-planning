from datetime import datetime
from pathlib import Path
import uuid

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends

from app.core.config import settings
from app.api.deps import PlanningStore, get_planning_store
from app.models.schemas import UploadResponse, HistoryEntryType
from app.services.pdf_parser import pdf_parser
from app.services.excel_handler import excel_handler
from app.services.ai_planner import ai_planner

router = APIRouter()


@router.post("/pdf", response_model=UploadResponse)
async def upload_pdf(
    file: UploadFile = File(...),
    process_with_ai: bool = True,
    store: PlanningStore = Depends(get_planning_store),
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Save uploaded file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id = str(uuid.uuid4())
    file_path = settings.upload_path / f"pdf_{timestamp}_{file_id[:8]}.pdf"

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        store.add_uploaded_file(file_path)

        # Process with AI if requested
        if process_with_ai:
            pdf_content = pdf_parser.extract_all(file_path)
            planning = ai_planner.process_pdf_content(
                pdf_text=pdf_content["text"],
                pdf_tables=pdf_content["tables"],
            )
            store.current_planning = planning

            # Save as Excel
            excel_path = settings.template_path / f"planning_{file_id}.xlsx"
            wb = excel_handler.create_planning_workbook(planning)
            excel_handler.save_workbook(wb, excel_path)
            store.planning_file = excel_path

        # Add history entry
        store.add_history_entry(
            entry_type=HistoryEntryType.IMPORT_PDF,
            filename=file.filename,
            week_number=store.current_planning.week_number if store.current_planning else None,
            year=store.current_planning.year if store.current_planning else None,
        )

        return UploadResponse(
            success=True,
            message="PDF uploaded and processed successfully" if process_with_ai else "PDF uploaded successfully",
            file_id=file_id,
            filename=file.filename,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.post("/excel", response_model=UploadResponse)
async def upload_excel(
    file: UploadFile = File(...),
    store: PlanningStore = Depends(get_planning_store),
):
    if not file.filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="File must be an Excel file (.xlsx or .xls)")

    # Save uploaded file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_id = str(uuid.uuid4())
    file_ext = Path(file.filename).suffix
    file_path = settings.upload_path / f"excel_{timestamp}_{file_id[:8]}{file_ext}"

    try:
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        store.add_uploaded_file(file_path)

        # Load planning from Excel
        planning = excel_handler.load_planning_from_excel(file_path)
        store.current_planning = planning
        store.planning_file = file_path

        # Add history entry
        store.add_history_entry(
            entry_type=HistoryEntryType.IMPORT_EXCEL,
            filename=file.filename,
            week_number=planning.week_number if planning else None,
            year=planning.year if planning else None,
        )

        return UploadResponse(
            success=True,
            message="Excel file uploaded and loaded successfully",
            file_id=file_id,
            filename=file.filename,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
