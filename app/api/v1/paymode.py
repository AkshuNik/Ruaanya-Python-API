from fastapi import APIRouter, Depends, HTTPException
from app.models.paymode_model import PaymodeCreate, PaymodeUpdate
from app.services.paymode_service import PaymodeService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/paymode", tags=["Paymode"])

@router.post("/create")
async def create_paymode(data: PaymodeCreate, user: dict = Depends(get_current_user)):
    return await PaymodeService.create(data, user["_id"])

@router.get("/list")
async def list_paymodes(user: dict = Depends(get_current_user)):
    return await PaymodeService.list()

@router.put("/update")
async def update_paymode(data: PaymodeUpdate, user: dict = Depends(get_current_user)):
    return await PaymodeService.update(data, user["_id"])

@router.delete("/delete/{id}")
async def delete_paymode(id: str, user: dict = Depends(get_current_user)):
    return await PaymodeService.delete(id)
