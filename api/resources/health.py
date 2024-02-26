from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
def echo():
    return {"message": "API is working"}
