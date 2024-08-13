from pydantic import BaseModel, Field
from typing import Optional

class QueryParams(BaseModel):
    limit: int = 10
    skip: int = 0

class DemoUserModel(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=40)
    email: str = Field(..., max_length=40, min_length=5)

    class Config:
        from_attributes = True
        orm_mode = True

class DemoLicenseModel(BaseModel):
    id: Optional[int] = None
    license_number: str = Field(..., max_length=15)
    is_active: bool = Field(..., default_factory=lambda : True)
    user_id: int = Field(...)

    class Config:
        from_attributes = True
        orm_mode = True


# Response Model
class DemoResponseUserModel(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=40)
    email: str = Field(..., max_length=40, min_length=5)
    licenses: list[DemoLicenseModel] = []
    class Config:
        from_attributes = True
        orm_mode = True

class DemoResponseLicenseModel(BaseModel):
    id: Optional[int] = None
    license_number: str = Field(..., max_length=15)
    is_active: bool = Field(..., default_factory=lambda : True)
    user: Optional[DemoUserModel] = Field(...)
    class Config:
        from_attributes = True
        orm_mode = True