from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.db.base import Estimate, EstimateItem, Material, Project
from backend.app.db.session import get_db
from backend.app.schemas.estimate import (
    EstimateBreakdownResponse,
    EstimateCreate,
    EstimateItemCreate,
    EstimateItemResponse,
    EstimateResponse,
    EstimateTotalResponse,
)

router = APIRouter(prefix="/estimates", tags=["Estimates"])


@router.post("/", response_model=EstimateResponse, status_code=201)
def create_estimate(
    estimate_data: EstimateCreate,
    db: Session = Depends(get_db),
):
    project = db.get(Project, estimate_data.project_id)

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    estimate = Estimate(**estimate_data.model_dump())

    db.add(estimate)
    db.commit()
    db.refresh(estimate)

    return estimate


@router.get("/", response_model=list[EstimateResponse])
def list_estimates(db: Session = Depends(get_db)):
    return db.scalars(
        select(Estimate).order_by(Estimate.id.desc())
    ).all()


@router.get("/{estimate_id}", response_model=EstimateResponse)
def get_estimate(
    estimate_id: int,
    db: Session = Depends(get_db),
):
    estimate = db.get(Estimate, estimate_id)

    if not estimate:
        raise HTTPException(
            status_code=404,
            detail="Estimate not found",
        )

    return estimate


@router.post(
    "/{estimate_id}/items",
    response_model=EstimateItemResponse,
    status_code=201,
)
def create_estimate_item(
    estimate_id: int,
    item_data: EstimateItemCreate,
    db: Session = Depends(get_db),
):
    estimate = db.get(Estimate, estimate_id)

    if not estimate:
        raise HTTPException(
            status_code=404,
            detail="Estimate not found",
        )

    if item_data.material_id is not None:
        material = db.get(Material, item_data.material_id)

        if not material:
            raise HTTPException(
                status_code=404,
                detail="Material not found",
            )

    amount = item_data.quantity * item_data.unit_rate

    item = EstimateItem(
        estimate_id=estimate_id,
        **item_data.model_dump(),
        amount=amount,
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item


@router.get(
    "/{estimate_id}/items",
    response_model=list[EstimateItemResponse],
)
def list_estimate_items(
    estimate_id: int,
    db: Session = Depends(get_db),
):
    estimate = db.get(Estimate, estimate_id)

    if not estimate:
        raise HTTPException(
            status_code=404,
            detail="Estimate not found",
        )

    return db.scalars(
        select(EstimateItem)
        .where(EstimateItem.estimate_id == estimate_id)
        .order_by(EstimateItem.id)
    ).all()


@router.get(
    "/{estimate_id}/total",
    response_model=EstimateTotalResponse,
)
def get_estimate_total(
    estimate_id: int,
    db: Session = Depends(get_db),
):
    estimate = db.get(Estimate, estimate_id)

    if not estimate:
        raise HTTPException(
            status_code=404,
            detail="Estimate not found",
        )

    result = db.execute(
        select(
            func.count(EstimateItem.id),
            func.coalesce(
                func.sum(EstimateItem.amount),
                Decimal("0"),
            ),
        ).where(
            EstimateItem.estimate_id == estimate_id
        )
    ).one()

    item_count, subtotal = result

    return EstimateTotalResponse(
        estimate_id=estimate_id,
        item_count=item_count,
        subtotal=subtotal,
    )


@router.get(
    "/{estimate_id}/breakdown",
    response_model=EstimateBreakdownResponse,
)
def get_estimate_breakdown(
    estimate_id: int,
    db: Session = Depends(get_db),
):
    estimate = db.get(Estimate, estimate_id)

    if not estimate:
        raise HTTPException(
            status_code=404,
            detail="Estimate not found",
        )

    rows = db.execute(
        select(
            EstimateItem.item_type,
            func.coalesce(func.sum(EstimateItem.amount), Decimal("0")),
        )
        .where(EstimateItem.estimate_id == estimate_id)
        .group_by(EstimateItem.item_type)
    ).all()

    material = Decimal("0")
    labour = Decimal("0")
    other = Decimal("0")

    for item_type, amount in rows:
        if item_type == "material":
            material += amount
        elif item_type == "labour":
            labour += amount
        else:
            other += amount

    subtotal = material + labour + other

    return EstimateBreakdownResponse(
        estimate_id=estimate_id,
        material=material,
        labour=labour,
        other=other,
        subtotal=subtotal,
    )