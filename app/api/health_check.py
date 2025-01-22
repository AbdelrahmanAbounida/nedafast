"""
    for health checking related to 
    - backend server 
    ...
"""
from fastapi import APIRouter


router = APIRouter(tags=["Health check"], prefix="/health")


@router.get("/")
async def check_health():
    return "I am running"