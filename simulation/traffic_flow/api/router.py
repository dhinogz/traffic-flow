from fastapi.routing import APIRouter
from api.system.views import router as system_router
from api.traffic_flow.views import router as traffic_router

api_router = APIRouter()
api_router.include_router(system_router, prefix="/system", tags=["system"])
api_router.include_router(traffic_router, prefix="/traffic", tags=["traffic-flow"])
