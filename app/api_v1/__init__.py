from fastapi import APIRouter

from .ml.views import router as ml_router
from .liker.views import router as liker_router


router = APIRouter()

router.include_router(router=ml_router)
router.include_router(router=liker_router)
