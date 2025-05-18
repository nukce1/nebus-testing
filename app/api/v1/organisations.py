from typing import (
    Annotated,
    List,
)

from dependencies.dependencies import get_organization_service
from domain.schemas import OrganizationRead
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    Security,
)
from protocols.service import OrganizationService
from security.authorization import verify_api_key
from services.exceptions import (
    OrganizationNotFoundException,
    StorageInternalException,
)
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

router = APIRouter(prefix="/organizations", tags=["organizations"], dependencies=[Security(verify_api_key)])


@router.get("/by-building/", response_model=List[OrganizationRead], status_code=HTTP_200_OK)
async def get_organizations_by_building_id_handler(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    building_id: int = Query(ge=1),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=20),
):
    """Returns a list of organizations by building id with pagination"""
    try:
        return await organization_service.get_organizations_by_building_id_with_pagination(building_id, page, limit)

    except StorageInternalException as exc:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    except OrganizationNotFoundException as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/by-activity/", response_model=List[OrganizationRead], status_code=HTTP_200_OK)
async def get_organizations_by_activity_id_handler(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    activity_id: int = Query(ge=1),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=20),
):
    """Returns a list of organizations by activity id with pagination"""
    try:
        return await organization_service.get_organizations_by_activity_id_with_pagination(activity_id, page, limit)

    except StorageInternalException as exc:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    except OrganizationNotFoundException as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/{organization_id}", response_model=OrganizationRead, status_code=HTTP_200_OK)
async def get_organization_by_id_handler(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    organization_id: Annotated[int, Path(ge=1)],
):
    """Returns an organization by id"""
    try:
        return await organization_service.get_organization_by_id(organization_id)

    except StorageInternalException as exc:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    except OrganizationNotFoundException as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/by-name/", response_model=OrganizationRead, status_code=HTTP_200_OK)
async def get_organization_by_name_handler(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    name: str = Query(min_length=1),
):
    """Returns an organization by name"""
    try:
        return await organization_service.get_organization_by_name(name)

    except StorageInternalException as exc:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    except OrganizationNotFoundException as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/in-radius/", response_model=List[OrganizationRead], status_code=HTTP_200_OK)
async def get_organizations_in_radius_handler(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    latitude: float = Query(ge=-90, le=90),
    longitude: float = Query(ge=-180, le=180),
    radius: float = Query(ge=0, le=1000, description="Radius in kilometers"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=20),
):
    """Returns a list of organizations in radius with pagination"""
    try:
        return await organization_service.get_organizations_in_radius_with_pagination(
            latitude, longitude, radius, page, limit
        )

    except StorageInternalException as exc:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    except OrganizationNotFoundException as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/in-bbox/", response_model=List[OrganizationRead], status_code=HTTP_200_OK)
async def get_organizations_in_bbox_handler(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    lat_min: float = Query(ge=-90, le=90),
    lon_min: float = Query(ge=-180, le=180),
    lat_max: float = Query(ge=-90, le=90),
    lon_max: float = Query(ge=-180, le=180),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=20),
):
    """Returns a list of organizations in bounding box with pagination"""
    try:
        return await organization_service.get_organizations_in_bbox_with_pagination(
            lat_min, lon_min, lat_max, lon_max, page, limit
        )

    except StorageInternalException as exc:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    except OrganizationNotFoundException as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(exc))


@router.get("/by-nested-activity/", response_model=List[OrganizationRead], status_code=HTTP_200_OK)
async def get_organizations_by_nested_activity_id_handler(
    organization_service: Annotated[OrganizationService, Depends(get_organization_service)],
    activity_id: int = Query(ge=1),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=20),
):
    """Returns a list of organizations with nested activities by activity id with pagination"""
    try:
        return await organization_service.get_organizations_by_nested_activity_id_with_pagination(
            activity_id, page, limit
        )

    except StorageInternalException as exc:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc))
    except OrganizationNotFoundException as exc:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(exc))
