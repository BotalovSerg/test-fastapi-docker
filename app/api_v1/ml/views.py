from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.models import db_helper
from app.analyser.cv_analiser import download_file, get_result
from .schemas import UserSchema, CVSchema
from app.crud import userprofile as crud_userprofile


router = APIRouter(tags=["ML Model"])


@router.get("/check/")
async def get_status(session: AsyncSession = Depends(db_helper.sesion_getter)):
    result = await crud_userprofile.test_connection(session=session)
    return {"message": {"status": "ok", "Test connect database": bool(result)}}


@router.post("/user/")
def get_user(user: UserSchema):
    return {"message": {"user": user}}


@router.post("/model-response/")
async def get_answer_ml_model(file: CVSchema):

    path_cv = await download_file(file.file_id)
    result = get_result(requirements="python, ml, linux", path_cv=path_cv)

    return {"message": result}
