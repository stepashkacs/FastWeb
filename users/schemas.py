from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(20)]
    # username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr