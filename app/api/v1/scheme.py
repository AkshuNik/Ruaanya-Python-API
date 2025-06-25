from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.scheme_model import SchemeCreate, SchemeUpdate, SchemeBase
from app.services.scheme_service import SchemeService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/scheme", tags=["Scheme"])

@router.post("/create")
async def create_scheme(data: SchemeCreate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await SchemeService.create_scheme(data)

# @router.get("/list", response_model=List[SchemeBase])
# async def get_schemes(user: dict = Depends(get_current_user)):
#     return await SchemeService.get_schemes()

@router.get("/list", response_model=List[SchemeBase])
async def list_schemes(status: str = None):
    return await SchemeService.get_schemes(status)


@router.put("/update")
async def update_scheme(data: SchemeUpdate, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await SchemeService.update_scheme(data)

@router.delete("/delete/{id}")
async def delete_scheme(id: str, user: dict = Depends(get_current_user)):
    if user.get("role_id") != 0:
        raise HTTPException(status_code=403, detail="Forbidden")
    return await SchemeService.delete_scheme(id)
