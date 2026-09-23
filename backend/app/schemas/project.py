from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    owner_id: int = Field(gt=0)
    location_id: int | None = Field(default=None, gt=0)
    name: str = Field(min_length=2, max_length=200)
    project_type: str = Field(min_length=2, max_length=50)
    status: str = Field(default="draft", min_length=2, max_length=30)
    client_name: str | None = Field(default=None, max_length=200)
    notes: str | None = Field(default=None, max_length=2000)


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
    plot_area_sqft: Decimal | None = Field(default=None, gt=0)
    built_up_area_sqft: Decimal | None = Field(default=None, gt=0)
    floors: int = Field(default=1, ge=1, le=100)
    bedrooms: int = Field(default=0, ge=0, le=100)
    bathrooms: int = Field(default=0, ge=0, le=100)
    kitchens: int = Field(default=1, ge=0, le=50)
    balconies: int = Field(default=0, ge=0, le=100)
    parking_spaces: int = Field(default=0, ge=0, le=100)
    construction_type: str | None = Field(default=None, max_length=100)
    site_conditions: str | None = Field(default=None, max_length=2000)


class ProjectSiteResponse(ProjectSiteCreate):
    id: int
    project_id: int

    model_config = ConfigDict(from_attributes=True)