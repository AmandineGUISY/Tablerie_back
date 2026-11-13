from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.Dto.restoDto import RestoRegister
from app.Service.restoService import authenticate_resto, register_resto
from app.Service.tokenService import get_current_resto

router = APIRouter(prefix="/auth/resto", tags=["auth"])

@router.post("/login")
async def api_login_resto(form_data: OAuth2PasswordRequestForm = Depends()):
    token = authenticate_resto(form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/register")
async def api_register_resto(user_data: RestoRegister):
    result = register_resto(user_data)
    if result["status_code"] != 200:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])
    return {"message": result["message"]}


@router.get("/me")
async def api_get_current_resto(resto_id: str = Depends(get_current_resto)):
    return {"resto_id": resto_id}
