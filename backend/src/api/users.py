from fastapi import APIRouter

from .dependencies import UoWDep

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def get_users(uow: UoWDep):
    ...
