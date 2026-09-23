from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.base import Material
from backend.app.db.session import get_db
from backend.app.schemas.material import MaterialResponse

router = APIRouter(prefix="/materials", tags=["Materials"])


@router.get("", response_model=list[MaterialResponse])
def get_materials(db: Session = Depends(get_db)):
    return db.scalars(
        select(Material).order_by(Material.category, Material.name)
    ).all()