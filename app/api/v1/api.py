from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.api_model import ApiBase, ApiCreate, ApiUpdate
from app.services.api_service import ApiService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/api", tags=["API"])

@router.post("/create")
async def create_api(data: ApiCreate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await ApiService.create_api(data)

@router.get("/list", response_model=List[ApiBase])
async def get_all_apis(user: dict = Depends(get_current_user)):
    return await ApiService.get_all_apis()

@router.put("/update")
async def update_api(data: ApiUpdate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await ApiService.update_api(data)

@router.delete("/delete/{id}")
async def delete_api(id: str, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await ApiService.delete_api(id)
