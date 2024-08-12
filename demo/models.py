from pydantic import BaseModel, Field
from typing import Optional

class QueryParams(BaseModel):
    limit: int = 10
    skip: int = 0

class DemoUserModel(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=40)
    email: str = Field(..., max_length=40, min_length=5, pattern='/^[a-zA-Z0-9. _-]+@[a-zA-Z0-9. -]+\. [a-zA-Z]{2,4}$/')

    class Config:
        from_attributes = True

class DemoLicenseModel(BaseModel):
    id: Optional[int] = None
    license_number: str = Field(..., max_length=15)
    isActive: bool = True
    user: DemoUserModel

    class Config:
        from_attributes = True