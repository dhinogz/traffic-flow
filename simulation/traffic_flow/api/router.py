from fastapi.routing import APIRouter
from api.system.views import router as system_router
from api.virus.views import router as virus_router
from api.flock.views import router as flock_router

api_router = APIRouter()
api_router.include_router(system_router, prefix="/system", tags=["system"])
api_router.include_router(virus_router, prefix="/traffic", tags=["traffic-flow"])
api_router.include_router(virus_router, prefix="/virus", tags=["virus-model"])
api_router.include_router(flock_router, prefix="/flock", tags=["flock"])