from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.api.documents import router as documents_router


class HealthResponse(BaseModel):
    status: Literal["ok"]


router = APIRouter()
router.include_router(documents_router)


@router.get("/health", response_model=HealthResponse, tags=["health"])
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
