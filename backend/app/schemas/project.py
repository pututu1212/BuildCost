from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    owner_id: int
    location_id: int | None = None
    name: str
    project_type: str
    status: str = "draft"
    client_name: str | None = None
    notes: str | None = None


class ProjectResponse(BaseModel):
    id: int
    owner_id: int
    location_id: int | None = None
    name: str
    project_type: str
    status: str
    client_name: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectSiteCreate(BaseModel):
    plot_area_sqft: Decimal | None = None
    built_up_area_sqft: Decimal | None = None
    floors: int = 1
    bedrooms: int = 0
    bathrooms: int = 0
    kitchens: int = 1
    balconies: int = 0
    parking_spaces: int = 0
    construction_type: str | None = None
    site_conditions: str | None = None


class ProjectSiteResponse(ProjectSiteCreate):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)