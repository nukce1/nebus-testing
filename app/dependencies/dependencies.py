from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db_session
from protocols.service import OrganizationService
from protocols.storage import Storage
from repository.postgres_repo import PostgresStorage
from services.organization_service import CustomOrganizationService


async def get_storage(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> Storage:
    return PostgresStorage(session)

async def get_organization_service(
    storage: Annotated[Storage, Depends(get_storage)],
) -> OrganizationService:
    return CustomOrganizationService(storage)