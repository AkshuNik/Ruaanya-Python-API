from fastapi import APIRouter, Depends, HTTPException
from app.services.apitoken_service import ApiTokenService
from app.models.apitoken_model import ApitokenCreate, CallbackUpdate, CompanyCodeUpdate
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/v1/apitoken", tags=["API Token"])


@router.post("/create")
async def create_apitoken(data: ApitokenCreate, user: dict = Depends(get_current_user)):
    result = await ApiTokenService.create_token(data, user["_id"])
    if result.get("status") != "success":
        raise HTTPException(status_code=400, detail=result.get("status"))
    return result


@router.get("/list")
async def list_apitokens(user: dict = Depends(get_current_user)):
    return await ApiTokenService.get_apitokens(user["_id"])


@router.put("/callback")
async def update_callback(data: CallbackUpdate, user: dict = Depends(get_current_user)):
    result = await ApiTokenService.update_callback(user["_id"], data.callbackurl)
    if result.get("status") != "success":
        raise HTTPException(status_code=400, detail=result.get("status"))
    return result


@router.put("/companycode")
async def update_company_code(data: CompanyCodeUpdate, user: dict = Depends(get_current_user)):
    return await ApiTokenService.update_company_code(user["_id"], data.companycode)

@router.delete("/delete/{token_id}")
async def delete_apitoken(token_id: str, current_user=Depends(get_current_user)):
    # Optional: add permission check if required
    return await ApiTokenService.delete_token(token_id)