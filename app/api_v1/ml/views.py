from fastapi import APIRouter

from app.analyser.cv_analiser import download_file, get_result
from .schemas import UserSchema, CVSchema

router = APIRouter(tags=["ML Model"])


@router.get("/check/")
def get_status():
    return {"message": "ok"}


@router.post("/user/")
def get_user(user: UserSchema):
    return {"message": {"user": user}}


@router.post("/model-response/")
async def get_answer_ml_model(file: CVSchema):

    path_cv = await download_file(file.file_id)
    result = get_result(requirements="python, ml, linux", path_cv=path_cv)

    return {"message": result}
