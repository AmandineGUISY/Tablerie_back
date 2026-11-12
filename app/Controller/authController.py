from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.Dto.customerDto import CustomerRegister
from app.Service.customerService import register_customer

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
 
@router.post("/register")
async def api_register_customer(user_data: CustomerRegister):
    result = register_customer(user_data)
    if result["status_code"] != 200:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])
    return {"message": result["message"]}

