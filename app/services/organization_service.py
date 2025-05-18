import logging

from domain.schemas import OrganizationRead
from protocols.storage import Storage
from services.exceptions import (
    OrganizationNotFoundException,
    StorageInternalException,
)


class CustomOrganizationService:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def get_organizations_by_building_id_with_pagination(
        self, building_id: int, page: int, limit: int
    ) -> list[dict]:
        """
        Returns a list of organizations by building id with pagination
        Args:
            building_id: Building id
            page: Page number
            limit: Limit of items per page

        Returns:
            list[dict]: List of organizations
        """
        try:
            organizations_dto: list[OrganizationRead] = (
                await self.storage.get_organizations_by_building_id_with_pagination(building_id, page, limit)
            )

        except Exception as exc:
            logging.error(
                f"Error while getting organizations from storage by building id {building_id} with pagination - {exc}"
            )
            raise StorageInternalException(message="Error while getting organizations from storage by building id")

        if not organizations_dto:
            raise OrganizationNotFoundException()

        organizations = [org.model_dump() for org in organizations_dto]

        return organizations

    async def get_organizations_by_activity_id_with_pagination(
        self, activity_id: int, page: int, limit: int
    ) -> list[dict]:
        """
        Returns a list of organizations by activity id with pagination
        Args:
            activity_id: Activity id
            page: Page number
            limit: Limit of items per page

        Returns:
            list[dict]: List of organizations
        """
        try:
            organizations_dto: list[OrganizationRead] = (
                await self.storage.get_organizations_by_activity_id_with_pagination(activity_id, page, limit)
            )
        except Exception as exc:
            logging.error(
                f"Error while getting organizations from storage by activity id {activity_id} with pagination - {exc}"
            )
            raise StorageInternalException(message="Error while getting organizations from storage by activity id")

        if not organizations_dto:
            raise OrganizationNotFoundException()

        organizations = [org.model_dump() for org in organizations_dto]

        return organizations

    async def get_organization_by_id(self, organization_id: int) -> dict:
        """
        Returns an organization by id
        Args:
            organization_id: Organization id

        Returns:
            dict: Organization
        """
        try:
            organization_dto: OrganizationRead = await self.storage.get_organization_by_id(organization_id)
        except Exception as exc:
            logging.error(f"Error while getting organization from storage by id {organization_id} - {exc}")
            raise StorageInternalException(message="Error while getting organization from storage by id")

        if not organization_dto:
            raise OrganizationNotFoundException()

        organization = organization_dto.model_dump()

        return organization

    async def get_organization_by_name(self, name: str) -> dict:
        """
        Returns an organization by name
        Args:
            name: Organization name

        Returns:
            dict: Organization
        """
        try:
            organization_dto: OrganizationRead = await self.storage.get_organization_by_name(name)
        except Exception as exc:
            logging.error(f"Error while getting organization from storage by name {name} - {exc}")
            raise StorageInternalException(message="Error while getting organization from storage by name")

        if not organization_dto:
            raise OrganizationNotFoundException()

        organization = organization_dto.model_dump()

        return organization

    async def get_organizations_in_radius_with_pagination(
        self, latitude: float, longitude: float, radius: float, page: int, limit: int
    ) -> list[dict]:
        """
        Returns a list of organizations in radius with pagination
        Args:
            latitude: Latitude
            longitude: Longitude
            radius: Radius in kilometers
            page: Page number
            limit: Limit of items per page

        Returns:
            list[dict]: List of organizations
        """
        try:
            organizations_dto: list[OrganizationRead] = await self.storage.get_organizations_in_radius_with_pagination(
                latitude, longitude, radius, page, limit
            )

        except Exception as exc:
            logging.error(f"Error while getting organizations from storage in radius with pagination - {exc}")
            raise StorageInternalException(
                message="Error while getting organizations from storage in radius with pagination"
            )

        if not organizations_dto:
            raise OrganizationNotFoundException()

        organizations = [org.model_dump() for org in organizations_dto]

        return organizations

    async def get_organizations_in_bbox_with_pagination(
        self, lat_min: float, lon_min: float, lat_max: float, lon_max: float, page: int, limit: int
    ) -> list[dict]:
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
            list[dict]: List of organizations
        """
        try:
            organizations_dto: list[OrganizationRead] = await self.storage.get_organizations_in_bbox_with_pagination(
                lat_min, lon_min, lat_max, lon_max, page, limit
            )
        except Exception as exc:
            logging.error(f"Error while getting organizations from storage in bounding box with pagination - {exc}")
            raise StorageInternalException(
                message="Error while getting organizations from storage in bounding box with pagination"
            )

        if not organizations_dto:
            raise OrganizationNotFoundException()

        organizations = [org.model_dump() for org in organizations_dto]

        return organizations

    async def get_organizations_by_nested_activity_id_with_pagination(
        self, activity_id: int, page: int, limit: int
    ) -> list[dict]:
        """
        Returns a list of organizations with nested activities by activity id with pagination
        Args:
            activity_id: Activity id
            page: Page number
            limit: Limit of items per page
        Returns:
            list[dict]: List of organizations
        """
        try:
            organizations_dto: list[OrganizationRead] = (
                await self.storage.get_organizations_by_nested_activity_id_with_pagination(activity_id, page, limit)
            )
        except Exception as exc:
            logging.error(
                f"Error while getting organizations from storage by nested activity id with pagination - {exc}"
            )
            raise StorageInternalException(
                message="Error while getting organizations from storage by nested activity id with pagination"
            )

        if not organizations_dto:
            raise OrganizationNotFoundException()

        organizations = [org.model_dump() for org in organizations_dto]

        return organizations
