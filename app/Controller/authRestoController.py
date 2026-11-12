from fastapi import APIRouter, HTTPException
from app.Dto.restoDto import RestoRegister
from app.Service.restoService import register_resto

router = APIRouter(prefix="/auth/resto", tags=["auth"])


@router.post("/register")
async def api_register_resto(user_data: RestoRegister):
    result = register_resto(user_data)
    if result["status_code"] != 200:
        raise HTTPException(status_code=result["status_code"], detail=result["message"])
    return {"message": result["message"]}
