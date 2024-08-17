from database.service import DatabaseService
from demo.models import DemoUserModel, DemoLicenseModel
from database.models.query_param_model import SQLQueryParam
from demo.schemas import DemoUser, DemoLicense
from fastapi import HTTPException

class DemoService:
    def __init__(self):
        self.user_service = DatabaseService(DemoUser)
    
    async def getAll(self, query: SQLQueryParam):
        return self.user_service.getAll(query)

    async def getOne(self, id: int):
        data = self.user_service.getOne(id)
        if data is None:
            raise HTTPException(status_code=404, detail=f"{id=} not found")
        return data
    
    async def saveOne(self, data:DemoUserModel):
        try:
            return self.user_service.saveOne(data.model_dump())
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    async def updateOne(self, id:str, data:DemoUserModel):
        try:
            if not self.user_service.getOne(id):
                raise HTTPException(status_code=404, detail=f'{id=} not found.')

            return self.user_service.updateOne(id, data.model_dump())
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e)) 
    
    async def saveLicenseOne(self, data: DemoLicenseModel):
        license_service = DatabaseService(DemoLicense)
        try:
            return license_service.saveOne(data.model_dump())
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
