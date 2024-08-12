from database.service import DatabaseService
from demo.models import QueryParams as RouterQueryParam
from database.models.query_param_model import SQLQueryParam
from demo.schemas import DemoUser

class DemoService:
    def __init__(self):
        self.user_service = DatabaseService(DemoUser)
    
    async def getAll(self, query: RouterQueryParam):
        query_params = SQLQueryParam.model_validate(query.model_dump())
        return self.user_service.getAll(query_params)