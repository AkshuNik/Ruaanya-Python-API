from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.auth import router as auth_router
from app.api.v1.member import router as member_router 
from app.api.v1.role import router as role_router 
from app.api.v1.permission import router as permission_router 
from app.api.v1.scheme import router as scheme_router 
from app.api.v1.api import router as api_router 
from app.api.v1.bank import router as bank_router 
from app.api.v1.apitoken import router as apitoken_router 
from app.api.v1.paymode import router as paymode_router
from app.api.v1.commission import router as commission_router
from app.api.v1.provider import router as provider_router
from app.api.v1.company import router as company_router
from app.api.v1.fundreport import router as fundreport_router
from app.api.v1.portal_setting import router as portal_setting_router
# from fastapi.staticfiles import StaticFiles

app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],   # POST, GET, OPTIONS sab allow hain
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(member_router)
app.include_router(role_router)
app.include_router(permission_router)
app.include_router(scheme_router)
app.include_router(api_router)
app.include_router(bank_router)
app.include_router(apitoken_router)
app.include_router(paymode_router)
app.include_router(commission_router)
app.include_router(provider_router)
app.include_router(company_router)
app.include_router(fundreport_router)
app.include_router(portal_setting_router)
# app.include_router(auth_router, prefix="/api/v1")
# app.include_router(member_router, prefix="/api/v1")
