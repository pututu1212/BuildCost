from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class EstimateCreate(BaseModel):
    project_id: int
    name: str
    version: int = 1
    status: str = "draft"
    notes: str | None = None


class EstimateResponse(BaseModel):
    id: int
    project_id: int
    name: str
    version: int
    status: str
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


class EstimateItemCreate(BaseModel):
    material_id: int | None = None
    item_type: str
    description: str
    quantity: Decimal
    unit_code: str
    unit_rate: Decimal
    amount: Decimal


class EstimateItemResponse(EstimateItemCreate):
    id: int
    estimate_id: int

    model_config = ConfigDict(from_attributes=True)