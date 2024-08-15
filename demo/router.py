from fastapi import APIRouter, Depends
from demo.service import DemoService
from database.models.query_param_model import SQLQueryParam
from demo.models import DemoUserModel, DemoUpdateUserModel, DemoLicenseModel, DemoResponseLicenseModel, DemoResponseUserModel
from typing import Annotated

router = APIRouter(prefix="/demo")

@router.get("", response_model=list[DemoResponseUserModel], response_model_exclude_unset=True)
async def getAll(query: Annotated[SQLQueryParam, Depends(SQLQueryParam)]):
    demo_service = DemoService()
    return await demo_service.getAll(query)

@router.get("/{id}", response_model=DemoResponseUserModel)
async def getOne(id: int):
    demo_service = DemoService()
    return await demo_service.getOne(id)

@router.patch('/{id}', response_model=DemoResponseUserModel)
async def updateOne(id: int, data: DemoUpdateUserModel):
    demo_service = DemoService()
    return await demo_service.updateOne(id, data)

@router.post("", response_model=DemoUserModel)
async def saveOne(data: DemoUserModel):
    demo_service = DemoService()
    return await demo_service.saveOne(data)

@router.post("/license", response_model=DemoResponseLicenseModel)
async def saveLicenseOne(data: DemoLicenseModel):
    demo_service = DemoService()
    return await demo_service.saveLicenseOne(data)
