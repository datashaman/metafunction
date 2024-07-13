from pydantic import BaseModel
from typing import Any, Dict, List, Optional, TypeVar, Generic


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    status: str = "success"
    data: Optional[T] = None


class FailResponse(BaseModel):
    status: str = "fail"
    data: Dict[str, Any]


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    code: Optional[int] = None
    data: Optional[Dict[str, Any]] = None
