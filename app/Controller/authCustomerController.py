from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.Dto.customerDto import CustomerRegister
from app.Service.customerService import authenticate_customer, register_customer
from app.Service.tokenService import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def api_login_customer(form_data: OAuth2PasswordRequestForm = Depends()):
    token = authenticate_customer(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/register")
async def api_register_customer(user_data: CustomerRegister):
    result = register_customer(user_data)
    if result["status_code"] != 200:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])
    return {"message": result["message"]}


@router.get("/me")
async def api_get_current_customer(customer_id: str = Depends(get_current_user)):
    return {"customer_id": customer_id}
