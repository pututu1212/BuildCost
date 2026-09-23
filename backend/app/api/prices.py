from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.base import MaterialPrice
from backend.app.db.session import get_db
from backend.app.schemas.price import PriceResponse

router = APIRouter(prefix="/prices", tags=["Prices"])


@router.get("", response_model=list[PriceResponse])
def get_prices(
    material_id: int | None = Query(default=None),
    location_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    query = select(MaterialPrice)

    if material_id is not None:
        query = query.where(MaterialPrice.material_id == material_id)

    if location_id is not None:
        query = query.where(MaterialPrice.location_id == location_id)

    query = query.order_by(MaterialPrice.observed_at.desc())

    return db.scalars(query).all()