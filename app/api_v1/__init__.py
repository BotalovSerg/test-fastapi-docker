from fastapi import APIRouter

from .ml.views import router as ml_router


router = APIRouter()

router.include_router(router=ml_router)
