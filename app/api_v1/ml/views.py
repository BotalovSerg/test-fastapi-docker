from fastapi import APIRouter

from .schemas import UserSchema

router = APIRouter(tags=["ML Model"])


@router.get("/check/")
def get_status():
    return {"message": "ok"}


@router.post("/user/")
def get_user(user: UserSchema):
    return {"message": {
        "user": user
    }}
