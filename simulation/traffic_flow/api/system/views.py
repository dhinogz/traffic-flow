from fastapi import APIRouter

# from models.models import info

router = APIRouter()


@router.get("/health/")
async def health() -> None:
    """
    Checks the health of a project.

    It returns 200 if the project is healthy.
    """


# @router.get("/info")
# async def get_model_info() -> dict:

#     return info
