"""insert test data

Revision ID: 56878999628a
Revises: d5b00d739644
Create Date: 2025-05-16 23:23:15.722843

"""

from typing import (
    Sequence,
    Union,
)

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "56878999628a"
down_revision: Union[str, None] = "cee65ab47b2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insert test data to the activities table
    op.bulk_insert(
        sa.table(
            "activities",
            sa.column("id", sa.Integer),
            sa.column("name", sa.String),
        ),
        [
            {"id": 1, "name": "Еда"},
            {"id": 2, "name": "Мясная продукция"},
            {"id": 3, "name": "Молочная продукция"},
            {"id": 4, "name": "Автомобили"},
            {"id": 5, "name": "Грузовые"},
            {"id": 6, "name": "Легковые"},
            {"id": 7, "name": "Запчасти"},
            {"id": 8, "name": "Аксессуары"},
        ],
    )

    # Insert test data to the activities_closures table
    op.bulk_insert(
        sa.table(
            "activities_closures",
            sa.column("id", sa.Integer),
            sa.column("ancestor_id", sa.Integer),
            sa.column("descendant_id", sa.Integer),
            sa.column("depth", sa.Integer),
        ),
        [
            {"id": 1, "ancestor_id": 1, "descendant_id": 2, "depth": 1},
            {"id": 2, "ancestor_id": 1, "descendant_id": 3, "depth": 1},
            {"id": 3, "ancestor_id": 4, "descendant_id": 8, "depth": 2},
            {"id": 4, "ancestor_id": 4, "descendant_id": 5, "depth": 1},
            {"id": 5, "ancestor_id": 4, "descendant_id": 6, "depth": 1},
            {"id": 6, "ancestor_id": 4, "descendant_id": 7, "depth": 2},
            {"id": 7, "ancestor_id": 6, "descendant_id": 7, "depth": 1},
            {"id": 8, "ancestor_id": 6, "descendant_id": 8, "depth": 1},
            {"id": 9, "ancestor_id": 1, "descendant_id": 1, "depth": 0},
            {"id": 10, "ancestor_id": 2, "descendant_id": 2, "depth": 0},
            {"id": 11, "ancestor_id": 3, "descendant_id": 3, "depth": 0},
            {"id": 12, "ancestor_id": 4, "descendant_id": 4, "depth": 0},
            {"id": 13, "ancestor_id": 5, "descendant_id": 5, "depth": 0},
            {"id": 14, "ancestor_id": 6, "descendant_id": 6, "depth": 0},
            {"id": 15, "ancestor_id": 7, "descendant_id": 7, "depth": 0},
            {"id": 16, "ancestor_id": 8, "descendant_id": 8, "depth": 0},
        ],
    )

    # Insert test data to the buildings table
    op.bulk_insert(
        sa.table(
            "buildings",
            sa.column("id", sa.Integer),
            sa.column("address", sa.String),
            sa.column("latitude", sa.Float),
            sa.column("longitude", sa.Float),
        ),
        [
            {"id": 1, "address": "г. Москва, ул. Ленина 1, офис 1", "latitude": 55.75222, "longitude": 37.62778},
            {"id": 2, "address": "г. Москва, ул. Ленина 2, офис 2", "latitude": 55.76222, "longitude": 37.63778},
            {"id": 3, "address": "г. Москва, ул. Ленина 3, офис 3", "latitude": 55.77222, "longitude": 37.64778},
            {"id": 4, "address": "г. Москва, ул. Ленина 4, офис 4", "latitude": 56.76222, "longitude": 38.63778},
            {"id": 5, "address": "г. Москва, ул. Ленина 55, офис 55", "latitude": 80.76222, "longitude": 60.63778},
            {"id": 6, "address": "г. Москва, ул. Ленина 65, офис 65", "latitude": 88.76222, "longitude": 66.63778},
            {"id": 7, "address": "г. Москва, ул. Ленина 10, офис 10", "latitude": 57.76222, "longitude": 39.63778},
            {"id": 8, "address": "г. Москва, ул. Ленина 15, офис 15", "latitude": 58.76222, "longitude": 40.63778},
        ],
    )

    # Insert test data to the organizations table
    op.bulk_insert(
        sa.table(
            "organizations",
            sa.column("id", sa.Integer),
            sa.column("name", sa.String),
            sa.column("phone", sa.String),
            sa.column("building_id", sa.Integer),
            sa.column("activity_id", sa.Integer),
        ),
        [
            {"id": 1, "name": "ООО Рога и Копыта", "phone": "2-222-222, 3-333-333, 8-923-666-13-13", "building_id": 1},
            {"id": 2, "name": "ООО Рога и Рога", "phone": "2-222-222", "building_id": 1},
            {"id": 3, "name": "ООО Копыта и Копыта", "phone": "3-333-333", "building_id": 1},
            {"id": 4, "name": "ООО И и И", "phone": "8-923-666-13-13", "building_id": 2},
            {"id": 5, "name": "ООО Рог и Копыто", "phone": "2-222-222, 3-333-333, 8-923-666-13-13", "building_id": 2},
            {
                "id": 6,
                "name": "ООО Здесь может быть ваша реклама",
                "phone": "2-222-222, 3-333-333, 8-923-666-13-13",
                "building_id": 3,
            },
            {"id": 7, "name": "ООО ООО ООО", "phone": "2-222-222, 3-333-333, 8-923-666-13-13", "building_id": 4},
            {"id": 8, "name": "ООО Рога Копыта", "phone": "2-222-222, 3-333-333, 8-923-666-13-13", "building_id": 5},
            {"id": 9, "name": "ООО Еда", "phone": "2-222-222, 3-333-333, 8-923-666-13-13", "building_id": 6},
            {"id": 10, "name": "ООО Автомобили", "phone": "2-222-222, 3-333-333, 8-923-666-13-13", "building_id": 6},
            {
                "id": 11,
                "name": "ОООЕда и Автомобили",
                "phone": "2-222-222, 3-333-333, 8-923-666-13-13",
                "building_id": 6,
            },
        ],
    )

    op.bulk_insert(
        sa.table(
            "organization_activity",
            sa.column("organization_id", sa.Integer),
            sa.column("activity_id", sa.Integer),
        ),
        [
            {"organization_id": 1, "activity_id": 1},
            {"organization_id": 2, "activity_id": 2},
            {"organization_id": 3, "activity_id": 3},
            {"organization_id": 4, "activity_id": 4},
            {"organization_id": 5, "activity_id": 5},
            {"organization_id": 6, "activity_id": 6},
            {"organization_id": 7, "activity_id": 7},
            {"organization_id": 8, "activity_id": 8},
            {"organization_id": 9, "activity_id": 1},
            {"organization_id": 9, "activity_id": 2},
            {"organization_id": 9, "activity_id": 3},
            {"organization_id": 10, "activity_id": 4},
            {"organization_id": 10, "activity_id": 5},
            {"organization_id": 10, "activity_id": 6},
            {"organization_id": 10, "activity_id": 7},
            {"organization_id": 10, "activity_id": 8},
            {"organization_id": 11, "activity_id": 1},
            {"organization_id": 11, "activity_id": 2},
            {"organization_id": 11, "activity_id": 3},
            {"organization_id": 11, "activity_id": 4},
            {"organization_id": 11, "activity_id": 5},
            {"organization_id": 11, "activity_id": 6},
            {"organization_id": 11, "activity_id": 7},
            {"organization_id": 11, "activity_id": 8},
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("organizations")
    op.drop_table("buildings")
    op.drop_table("activities_closures")
    op.drop_table("activities")
