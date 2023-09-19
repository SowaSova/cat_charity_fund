from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.utils import investing_process
from app.api.endpoints.validators import (
    check_charity_project_before_delete,
    check_charity_project_before_update,
    check_charity_project_exists,
    check_name_duplicate,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)

router = APIRouter()


@router.get(
    "/",
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_charity_projects = await charity_project_crud.get_multi(session)
    return all_charity_projects


@router.post(
    "/",
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create_obj_with_datetime(
        project, session
    )
    await investing_process(new_project, Donation, session)
    return new_project


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_charity_project_exists(project_id, session)
    project = await check_charity_project_before_update(
        project_id, obj_in, session
    )
    project_update = await charity_project_crud.update(
        project, obj_in, session
    )
    return project_update


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_charity_project_exists(project_id, session)
    project = await check_charity_project_before_delete(project_id, session)
    project = await charity_project_crud.remove(project, session)
    return project
