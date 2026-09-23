from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class PriceResponse(BaseModel):
    id: int
    material_id: int
    location_id: int | None = None
    source_id: int | None = None
    supplier_id: int | None = None
    price: Decimal
    currency: str
    observed_at: datetime
    valid_until: datetime | None = None

    model_config = ConfigDict(from_attributes=True)