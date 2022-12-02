from fastapi.routing import APIRouter
from api.traffic_flow.views import router as traffic_router

api_router = APIRouter()
api_router.include_router(traffic_router, prefix="/traffic", tags=["traffic-flow"])


@api_router.get("/system/health/")
async def health() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """
