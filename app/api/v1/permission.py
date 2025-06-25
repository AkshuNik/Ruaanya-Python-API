from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import get_current_user
from app.services.permission_service import PermissionService
from app.models.permission_model import PermissionCreate, PermissionUpdate, PermissionBase
from typing import List

router = APIRouter(prefix="/api/v1/permission", tags=["Permission"])

@router.post("/create")
async def create_permission(data: PermissionCreate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await PermissionService.create_permission(data)

@router.get("/list", response_model=List[PermissionBase])
async def get_permissions(user: dict = Depends(get_current_user)):
    return await PermissionService.get_permissions()

@router.put("/update")
async def update_permission(data: PermissionUpdate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await PermissionService.update_permission(data)

@router.delete("/delete/{id}")
async def delete_permission(id: str, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await PermissionService.delete_permission(id)
