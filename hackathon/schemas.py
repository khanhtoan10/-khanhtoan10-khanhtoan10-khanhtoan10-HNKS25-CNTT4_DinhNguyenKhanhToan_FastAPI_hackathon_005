from pydantic import BaseModel
from pydantic import BaseModel
from typing import Optional, Any


class BookBase(BaseModel):
    title: str
    author: str
    category: str
    quantity: int


class BaseResponse(BaseModel):
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[Any] = None
