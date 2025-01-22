from pydantic import BaseModel
from typing import Generic, TypeVar


T = TypeVar('T')

class UnifiedResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str = "Success"
    data: T | None = None
    error: bool = False
