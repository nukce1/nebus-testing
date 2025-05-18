from domain.models import (
    Activity,
    ActivityClosure,
    Building,
    Organization,
    organization_activity,
)
from domain.schemas import OrganizationRead
from repository.constants import (
    EARTH_RADIUS_KM,
    NESTED_DEPTH,
)
from sqlalchemy import (
    distinct,
    func,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    joinedload,
    selectinload,
)


class PostgresStorage:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_organizations_by_building_id_with_pagination(
        self, building_id: int, page: int, limit: int
    ) -> list[OrganizationRead] | None:
        """
        Returns a list of organizations by building id with pagination
        Args:
            building_id: Building id
            page: Page number
            limit: Limit of items per page

        Returns:
            list[OrganizationRead]: List of organizations
        """
        offset: int = (page - 1) * limit
        query = (
            select(Organization)
            .options(joinedload(Organization.building), selectinload(Organization.activities))
            .filter_by(building_id=building_id)
            .order_by(Organization.id)
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        organizations_orm = list(result.scalars().all())

        if not result:
            return

        organizations_dto = [
            OrganizationRead(
                id=organization.id,
                name=organization.name,
                phone=organization.phone,
                building_address=organization.building.address,
                activities=[activity.name for activity in organization.activities],
            )
            for organization in organizations_orm
        ]

        return organizations_dto

    async def get_organizations_by_activity_id_with_pagination(
        self, activity_id: int, page: int, limit: int
    ) -> list[OrganizationRead] | None:
        """
        Returns a list of organizations by activity id with pagination
        Args:
            activity_id: Activity id
            page: Page number
            limit: Limit of items per page

        Returns:
            list[OrganizationRead]: List of organizations

        """
        offset: int = (page - 1) * limit
        query = (
            select(Organization)
            .join(Organization.activities)
            .filter(Activity.id == activity_id)
            .options(joinedload(Organization.building), selectinload(Organization.activities))
            .order_by(Organization.id)
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        organizations_orm = list(result.scalars().all())

        if not result:
            return

        organizations_dto = [
            OrganizationRead(
                id=organization.id,
                name=organization.name,
                phone=organization.phone,
                building_address=organization.building.address,
                activities=[activity.name for activity in organization.activities],
            )
            for organization in organizations_orm
        ]

        return organizations_dto

    async def get_organization_by_id(self, organization_id: int) -> OrganizationRead | None:
        """
        Returns an organization by id
        Args:
            organization_id: Organization id

        Returns:
            OrganizationRead: Organization
        """
        query = (
            select(Organization)
            .where(Organization.id == organization_id)
            .options(joinedload(Organization.building), selectinload(Organization.activities))
        )

        result = await self.session.execute(query)

        organization_orm = result.scalars().first()

        if not organization_orm:
            return

        organization_dto = OrganizationRead(
            id=organization_orm.id,
            name=organization_orm.name,
            phone=organization_orm.phone,
            building_address=organization_orm.building.address,
            activities=[activity.name for activity in organization_orm.activities],
        )

        return organization_dto

    async def get_organization_by_name(self, name: str) -> OrganizationRead | None:
        """
        Returns an organization by name
        Args:
            name: Organization name

        Returns:
            OrganizationRead: Organization
        """
        query = (
            select(Organization)
            .where(Organization.name == name)
            .options(joinedload(Organization.building), selectinload(Organization.activities))
        )

        result = await self.session.execute(query)

        organization_orm = result.scalars().first()

        if not organization_orm:
            return

        organization_dto = OrganizationRead(
            id=organization_orm.id,
            name=organization_orm.name,
            phone=organization_orm.phone,
            building_address=organization_orm.building.address,
            activities=[activity.name for activity in organization_orm.activities],
        )

        return organization_dto

    async def get_organizations_in_radius_with_pagination(
        self, latitude: float, longitude: float, radius: float, page: int, limit: int
    ) -> list[OrganizationRead] | None:
        """
        Returns a list of organizations in radius with pagination
        Args:
            latitude: Latitude
            longitude: Longitude
            radius: Radius in kilometers
            page: Page number
            limit: Limit of items per page

        Returns:
            list[OrganizationRead]: List of organizations
        """
        offset: int = (page - 1) * limit
        query = (
            select(Organization)
            .join(Organization.building)
            .filter(
                EARTH_RADIUS_KM
                * func.acos(
                    func.cos(func.radians(latitude))
                    * func.cos(func.radians(Building.latitude))
                    * func.cos(func.radians(Building.longitude) - func.radians(longitude))
                    + func.sin(func.radians(latitude)) * func.sin(func.radians(Building.latitude))
                )
                <= radius
            )
            .options(joinedload(Organization.building), selectinload(Organization.activities))
            .order_by(Organization.id)
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        organizations_orm = list(result.scalars().all())

        if not result:
            return

        organizations_dto = [
            OrganizationRead(
                id=organization.id,
                name=organization.name,
                phone=organization.phone,
                building_address=organization.building.address,
                activities=[activity.name for activity in organization.activities],
            )
            for organization in organizations_orm
        ]

        return organizations_dto

    async def get_organizations_in_bbox_with_pagination(
        self, lat_min: float, lon_min: float, lat_max: float, lon_max: float, page: int, limit: int
    ) -> list[OrganizationRead] | None:
        """
        Returns a list of organizations in bounding box with pagination
        Args:
            lat_min: Minimum latitude
            lon_min: Minimum longitude
            lat_max: Maximum latitude
            lon_max: Maximum longitude
            page: Page number
            limit: Limit of items per page
        Returns:
            list[OrganizationRead]: List of organizations
        """
        offset: int = (page - 1) * limit
        query = (
            select(Organization)
            .join(Organization.building)
            .filter(Building.latitude.between(lat_min, lat_max), Building.longitude.between(lon_min, lon_max))
            .options(joinedload(Organization.building), selectinload(Organization.activities))
            .order_by(Organization.id)
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(query)

        organizations_orm = list(result.scalars().all())

        if not result:
            return

        organizations_dto = [
            OrganizationRead(
                id=organization.id,
                name=organization.name,
                phone=organization.phone,
                building_address=organization.building.address,
                activities=[activity.name for activity in organization.activities],
            )
            for organization in organizations_orm
        ]

        return organizations_dto

    async def get_organizations_by_nested_activity_id_with_pagination(
        self, activity_id: int, page: int, limit: int
    ) -> list[OrganizationRead] | None:
        """
        Returns a list of organizations with nested activities by activity id with pagination
        Args:
            activity_id: Activity id
            page: Page number
            limit: Limit of items per page
        Returns:
            list[OrganizationRead]: List of organizations
        """
        offset: int = (page - 1) * limit

        ids_subq = (
            select(distinct(organization_activity.c.organization_id).label("org_id"))
            .join(ActivityClosure, organization_activity.c.activity_id == ActivityClosure.descendant_id)
            .where(ActivityClosure.ancestor_id == activity_id, ActivityClosure.depth <= NESTED_DEPTH)
            .order_by(organization_activity.c.organization_id)
            .offset(offset)
            .limit(limit)
            .subquery()
        )

        query = (
            select(Organization)
            .join(ids_subq, Organization.id == ids_subq.c.org_id)
            .options(joinedload(Organization.building), selectinload(Organization.activities))
            .order_by(Organization.id)
        )

        result = await self.session.execute(query)

        organizations_orm = list(result.scalars().all())

        if not result:
            return

        organizations_dto = [
            OrganizationRead(
                id=organization.id,
                name=organization.name,
                phone=organization.phone,
                building_address=organization.building.address,
                activities=[activity.name for activity in organization.activities],
            )
            for organization in organizations_orm
        ]

        return organizations_dto
