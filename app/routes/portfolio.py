from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_placeholder():
    return {"message": "Portfolio route ready to build "}