from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


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
    quantity: Decimal = Field(gt=0)
    unit_code: str
    unit_rate: Decimal = Field(ge=0)


class EstimateItemResponse(BaseModel):
    id: int
    estimate_id: int
    material_id: int | None = None
    item_type: str
    description: str
    quantity: Decimal
    unit_code: str
    unit_rate: Decimal
    amount: Decimal

    model_config = ConfigDict(from_attributes=True)


class EstimateTotalResponse(BaseModel):
    estimate_id: int
    item_count: int
    subtotal: Decimal


class EstimateBreakdownResponse(BaseModel):
    estimate_id: int
    material: Decimal
    labour: Decimal
    other: Decimal
    subtotal: Decimal