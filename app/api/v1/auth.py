from fastapi import APIRouter, Depends, Request
from app.services.auth_service import AuthService
from app.models.user_model import UserCreate, UserLogin
from fastapi import HTTPException
from app.middleware.auth import get_current_user


router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register")
async def register(user: UserCreate):
    return await AuthService.register_user(user)

@router.post("/login")
async def login(user: UserLogin):
    return await AuthService.login_user(user)

@router.post("/logout")
async def logout(request: Request, user: dict = Depends(get_current_user)):
    return await AuthService.logout_user(request)
