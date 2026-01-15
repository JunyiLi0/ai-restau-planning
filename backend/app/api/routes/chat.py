import uuid

from fastapi import APIRouter, HTTPException, Depends

from app.core.config import settings
from app.api.deps import PlanningStore, get_planning_store
from app.models.schemas import ChatMessage, ChatResponse
from app.services.ai_planner import ai_planner
from app.services.excel_handler import excel_handler

router = APIRouter()


@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: ChatMessage,
    store: PlanningStore = Depends(get_planning_store),
):
    try:
        response_text, new_planning = ai_planner.process_chat_message(
            message=message.message,
            current_planning=store.current_planning,
        )

        planning_updated = False
        if new_planning:
            store.current_planning = new_planning
            planning_updated = True

            # Save/update Excel file
            if store.planning_file:
                excel_handler.update_planning_in_excel(store.planning_file, new_planning)
            else:
                file_id = str(uuid.uuid4())
                excel_path = settings.template_path / f"planning_{file_id}.xlsx"
                wb = excel_handler.create_planning_workbook(new_planning)
                excel_handler.save_workbook(wb, excel_path)
                store.planning_file = excel_path

        return ChatResponse(
            response=response_text,
            planning_updated=planning_updated,
            planning=store.current_planning,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")
