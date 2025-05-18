from pydantic import BaseModel


class OrganizationRead(BaseModel):
    id: int
    name: str
    phone: str
    building_address: str
    activities: list[str]
