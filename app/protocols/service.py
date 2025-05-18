from typing import Protocol


class OrganizationService(Protocol):
    async def get_organizations_by_building_id_with_pagination(
        self, building_id: int, page: int, limit: int
    ) -> list[dict]: ...

    async def get_organizations_by_activity_id_with_pagination(
        self, activity_id: int, page: int, limit: int
    ) -> list[dict]: ...

    async def get_organization_by_id(self, organization_id: int) -> dict: ...

    async def get_organization_by_name(self, name: str) -> dict: ...

    async def get_organizations_in_radius_with_pagination(
        self, latitude: float, longitude: float, radius: float, page: int, limit: int
    ) -> list[dict]: ...

    async def get_organizations_in_bbox_with_pagination(
        self, lat_min: float, lon_min: float, lat_max: float, lon_max: float, page: int, limit: int
    ) -> list[dict]: ...

    async def get_organizations_by_nested_activity_id_with_pagination(
        self, activity_id: int, page: int, limit: int
    ) -> list[dict]: ...
