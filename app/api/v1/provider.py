from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.provider_model import ProviderBase, ProviderCreate, ProviderUpdate
from app.services.provider_service import ProviderService
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/provider", tags=["Provider"])

@router.post("/create")
async def create_provider(data: ProviderCreate, user: dict = Depends(get_current_user)):
    return await ProviderService.create_provider(data)

@router.get("/list", response_model=List[ProviderBase])
async def list_providers(user: dict = Depends(get_current_user)):
    return await ProviderService.get_all_providers()

@router.put("/update")
async def update_provider(data: ProviderUpdate, user: dict = Depends(get_current_user)):
    return await ProviderService.update_provider(data)

@router.delete("/delete/{id}")
async def delete_provider(id: str, user: dict = Depends(get_current_user)):
    return await ProviderService.delete_provider(id)
