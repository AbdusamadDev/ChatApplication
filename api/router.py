from fastapi import APIRouter

from .renderers.views import router as template_router
from .auth.views import router as auth_router
from .base.views import router as api_router

router = APIRouter(prefix="")

router.include_router(template_router)
router.include_router(auth_router)
router.include_router(api_router)
