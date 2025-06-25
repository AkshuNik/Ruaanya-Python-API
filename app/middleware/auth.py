# # from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# # from fastapi import Request, HTTPException, status
# # from jose import jwt, JWTError
# # from app.core.config import settings

# # class JWTBearer(HTTPBearer):
# #     def __init__(self, auto_error: bool = True):
# #         super(JWTBearer, self).__init__(auto_error=auto_error)

# #     async def __call__(self, request: Request):
# #         credentials: HTTPAuthorizationCredentials = await super().__call__(request)
# #         if credentials:
# #             if not self.verify_jwt(credentials.credentials):
# #                 raise HTTPException(
# #                     status_code=status.HTTP_403_FORBIDDEN,
# #                     detail="Invalid or expired token"
# #                 )
# #             return credentials.credentials
# #         else:
# #             raise HTTPException(
# #                 status_code=status.HTTP_403_FORBIDDEN,
# #                 detail="Authorization token missing"
# #             )

# #     def verify_jwt(self, token: str) -> bool:
# #         try:
# #             payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
# #             return True
# #         except JWTError:
# #             return False


# from fastapi import Depends, HTTPException, Request
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
# from jose import jwt, JWTError

# from app.utils.jwt import SECRET_KEY, ALGORITHM

# security = HTTPBearer()

# async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Invalid or expired token")

#     blacklisted = await db["token_blacklist"].find_one({"token": token})
#     if blacklisted:
#         raise HTTPException(status_code=401, detail="Token has been blacklisted")


from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from bson import ObjectId

from app.utils.jwt import SECRET_KEY, ALGORITHM
from app.db.mongo import db

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # ✅ Return full user with _id
        return {
            "_id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "role_id": user["role_id"]
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
