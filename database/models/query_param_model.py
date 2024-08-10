from pydantic import BaseModel
from typing import Optional

class SQLQueryParam(BaseModel):
    limit: int = 10
    skip: int = 0
    order_by: Optional[str] = None
    group_by: Optional[str] = None
    having: Optional[str] = None
    selected_fields: list[str] = []
    filter_by: str = None
