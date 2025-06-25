from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.portal_setting_model import PortalSettingCreate, PortalSettingUpdate, PortalSettingBase
from app.services.portal_setting_service import PortalSettingService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/portalsetting", tags=["PortalSetting"])

@router.post("/create")
async def create(data: PortalSettingCreate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await PortalSettingService.create(data)

@router.get("/list", response_model=List[PortalSettingBase])
async def list(user: dict = Depends(get_current_user)):
    return await PortalSettingService.list_all()

@router.put("/update")
async def update(data: PortalSettingUpdate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await PortalSettingService.update(data)

@router.delete("/delete/{id}")
async def delete(id: str, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await PortalSettingService.delete(id)
