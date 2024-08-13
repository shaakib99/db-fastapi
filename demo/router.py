from fastapi import APIRouter, Depends
from demo.service import DemoService
from demo.models import QueryParams, DemoUserModel, DemoLicenseModel, DemoResponseLicenseModel, DemoResponseUserModel
from typing import Annotated

router = APIRouter(prefix="/demo")

@router.get("")
async def getAll(query: Annotated[QueryParams, Depends(QueryParams)]):
    demo_service = DemoService()
    return await demo_service.getAll(query)

@router.get("/{id}", response_model=DemoResponseUserModel)
async def getOne(id: int):
    demo_service = DemoService()
    return await demo_service.getOne(id)

@router.post("", response_model=DemoUserModel)
async def saveOne(data: DemoUserModel):
    demo_service = DemoService()
    return await demo_service.saveOne(data)

@router.post("/license", response_model=DemoResponseLicenseModel)
async def saveLicenseOne(data: DemoLicenseModel):
    demo_service = DemoService()
    return await demo_service.saveLicenseOne(data)
