from domain.schemas import OrganizationRead
from pydantic import TypeAdapter

organization_adapter = TypeAdapter(OrganizationRead)

organizations_adapter = TypeAdapter(list[OrganizationRead])
