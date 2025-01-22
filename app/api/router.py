"""
    Main Router for different API Versions
"""

from fastapi import APIRouter
from app.api.v1 import items_router
from app.core.config import settings

from app.api.health_check import router as health_check_router

# *****************
# Version1 Routes
# *****************

router = APIRouter(
    prefix=f"/api/{settings.CURRENT_VERSION}"
)

# TODO >> register more routers here 
router.include_router(items_router)
router.include_router(health_check_router)