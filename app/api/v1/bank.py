from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.bank_model import BankBase, BankCreate, BankUpdate
from app.services.bank_service import BankService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/bank", tags=["Bank"])

@router.post("/create")
async def create_bank(data: BankCreate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await BankService.create_bank(data)

@router.get("/list", response_model=List[BankBase])
async def list_banks(user: dict = Depends(get_current_user)):
    return await BankService.get_all_banks()

@router.put("/update")
async def update_bank(data: BankUpdate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await BankService.update_bank(data)

@router.delete("/delete/{id}")
async def delete_bank(id: str, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await BankService.delete_bank(id)
