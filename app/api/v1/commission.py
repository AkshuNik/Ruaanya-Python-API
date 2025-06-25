from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.commission_model import CommissionBase, CommissionCreate, CommissionUpdate
from app.services.commission_service import CommissionService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/commission", tags=["Commission"])

@router.post("/create")
async def create_commission(data: CommissionCreate, user: dict = Depends(get_current_user)):
    return await CommissionService.create_commission(data)

@router.get("/list", response_model=List[CommissionBase])
async def list_commissions(user: dict = Depends(get_current_user)):
    return await CommissionService.get_all_commissions()

@router.put("/update")
async def update_commission(data: CommissionUpdate, user: dict = Depends(get_current_user)):
    return await CommissionService.update_commission(data)

@router.delete("/delete/{id}")
async def delete_commission(id: str, user: dict = Depends(get_current_user)):
    return await CommissionService.delete_commission(id)

@router.put("/update/{id}/{scheme_id}")
async def update_commission_by_scheme(id: str, scheme_id: str, body: dict):
    return await CommissionService.update_commission_by_id_and_scheme(id, scheme_id, body)

@router.get("/list/{scheme_id}")
async def list_commissions_by_scheme(scheme_id: str):
    commissions = await CommissionService.get_all_commissions(scheme_id)
    return commissions

