from pydantic import BaseModel, ConfigDict


class MaterialResponse(BaseModel):
    id: int
    name: str
    category: str
    specification: str | None = None
    default_unit_id: int | None = None

    model_config = ConfigDict(from_attributes=True)