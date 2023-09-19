from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.utils import investing_process
from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDB, DonationUser

router = APIRouter()


@router.post(
    "/",
    response_model=DonationUser,
    response_model_exclude_none=True,
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create_obj_with_datetime(
        donation, session, user
    )
    await investing_process(new_donation, CharityProject, session)
    return new_donation


@router.get(
    "/",
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    "/my",
    response_model=list[DonationUser],
    response_model_exclude={"user_id"},
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    donations = await donation_crud.get_by_user(session, user)
    return donations
