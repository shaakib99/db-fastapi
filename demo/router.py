from fastapi import APIRouter, Depends
from demo.service import DemoService
from demo.models import QueryParams

router = APIRouter(prefix="/demo")

@router.get("")
async def getAll(query: QueryParams = Depends(QueryParams)):
    demo_service = DemoService()
    return await demo_service.getAll(query)
