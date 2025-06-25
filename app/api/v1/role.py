from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.services.role_service import RoleService
from app.models.role_model import RoleCreate, RoleUpdate, RoleOut
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/role", tags=["Role"])

@router.post("/create")
async def create_role(data: RoleCreate, current_user: dict = Depends(get_current_user)):
    if current_user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await RoleService.create_role(data)

@router.get("/list", response_model=List[RoleOut])
async def list_roles(current_user: dict = Depends(get_current_user)):
    if current_user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await RoleService.get_all_roles()

@router.put("/update")
async def update_role(data: RoleUpdate, current_user: dict = Depends(get_current_user)):
    if current_user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await RoleService.update_role(data)

@router.delete("/delete/{role_id}")
async def delete_role(role_id: str, current_user: dict = Depends(get_current_user)):
    if current_user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await RoleService.delete_role(role_id)
