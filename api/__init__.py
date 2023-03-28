from fastapi import APIRouter 
from api.auth import router as auth_router
from api.shortener import router as shortener_router 


router = APIRouter()
router.include_router(auth_router,prefix="/auth", tags=["Authentication"])
router.include_router(shortener_router,)