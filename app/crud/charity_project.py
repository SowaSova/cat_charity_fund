from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    @staticmethod
    async def get_project_id_by_name(
        charity_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        charity_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == charity_name
            )
        )
        charity_id = charity_id.scalars().first()
        return charity_id


charity_project_crud = CRUDCharityProject(CharityProject)
