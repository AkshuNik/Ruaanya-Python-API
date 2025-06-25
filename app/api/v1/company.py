# app/api/v1/company.py (FastAPI router)
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.company_model import CompanyCreate, CompanyUpdate, CompanyBase
from app.services.company_service import CompanyService
from app.middleware.auth import get_current_user  # your auth dependency

router = APIRouter(prefix="/api/v1/company", tags=["Company Profile"])

@router.post("/create")
async def create_company(data: CompanyCreate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await CompanyService.create_company(data)

@router.get("/list", response_model=List[CompanyBase])
async def list_companies(user: dict = Depends(get_current_user)):
    return await CompanyService.get_all_companies()

@router.put("/update")
async def update_company(data: CompanyUpdate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await CompanyService.update_company(data)

@router.delete("/delete/{id}")
async def delete_company(id: str, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await CompanyService.delete_company(id)
