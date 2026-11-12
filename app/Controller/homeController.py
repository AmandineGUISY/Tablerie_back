from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/home", tags=["home"])
@router.post("/")
async def api_test_home():
    return {"message": "Tout va bien !", "status": 200}