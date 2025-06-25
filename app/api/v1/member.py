from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.models.user_model import UserBase
from app.models.user_model import MemberCreate
from app.services.member_service import MemberService
from app.middleware.auth import get_current_user
from typing import List
from app.models.user_model import ProfileUpdateRequest

router = APIRouter(prefix="/api/v1/member", tags=["Member"])

@router.post("/create")
async def create_member(data: MemberCreate, user: dict = Depends(get_current_user)):
    result = await MemberService.create_member(data, user)
    if result.get("status") != "success":
        raise HTTPException(status_code=400, detail=result.get("status"))
    return result

@router.get("/userlist", response_model=List[UserBase])
async def get_userlist(user: dict = Depends(get_current_user)):
    if user.get("role_id") != 1:
        raise HTTPException(status_code=403, detail="Unauthorized")

    members = await MemberService.get_all_members()
    return members

@router.get("/profile/{id}", response_model=UserBase)
async def get_user_settings(id: str = "0", current_user: dict = Depends(get_current_user)):
    return await MemberService.get_user_settings(id, current_user)

@router.post("/profileupdate")
async def profile_update(data: ProfileUpdateRequest, request: Request, current_user: dict = Depends(get_current_user)):
    result = await MemberService.profile_update(data, current_user)
    if result["status"] == "success":
        return result
    else:
        raise HTTPException(status_code=400, detail=result)