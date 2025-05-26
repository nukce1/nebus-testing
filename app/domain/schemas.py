from pydantic import (
    BaseModel,
    ConfigDict,
)


class ActivityRead(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class BuildingRead(BaseModel):
    address: str

    model_config = ConfigDict(from_attributes=True)


class OrganizationRead(BaseModel):
    id: int
    name: str
    phone: str
    building: BuildingRead
    activities: list[ActivityRead]

    model_config = ConfigDict(from_attributes=True)
