from fastapi import APIRouter

from app.api.routes.analyses import router as analyses_router


api_router = APIRouter(prefix="/api")
api_router.include_router(analyses_router)
