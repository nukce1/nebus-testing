from typing import Annotated

from database import get_db_session
from fastapi import Depends
from protocols.service import OrganizationService
from protocols.storage import Storage
from repository.postgres_repo import PostgresStorage
from services.organization_service import CustomOrganizationService
from sqlalchemy.ext.asyncio import AsyncSession


async def get_storage(session: Annotated[AsyncSession, Depends(get_db_session)]) -> Storage:
    return PostgresStorage(session)


async def get_organization_service(
    storage: Annotated[Storage, Depends(get_storage)],
) -> OrganizationService:
    return CustomOrganizationService(storage)
