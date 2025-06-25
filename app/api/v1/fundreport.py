from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.fundreport_model import FundReportCreate, FundReportUpdate, FundReportBase
from app.services.fundreport_service import FundReportService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/fundreport", tags=["FundReport"])

@router.post("/create")
async def create_fundreport(data: FundReportCreate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await FundReportService.create_fundreport(data)

@router.get("/list", response_model=List[FundReportBase])
async def list_fundreports(user: dict = Depends(get_current_user)):
    return await FundReportService.get_all_fundreports()

@router.put("/update")
async def update_fundreport(data: FundReportUpdate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await FundReportService.update_fundreport(data)

@router.delete("/delete/{id}")
async def delete_fundreport(id: str, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await FundReportService.delete_fundreport(id)
