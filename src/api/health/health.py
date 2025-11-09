from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get(path="/health")
async def health() -> str:
    return "I'm alive!"