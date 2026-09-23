from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    projects: Mapped[list["Project"]] = relationship(back_populates="owner")


class Location(TimestampMixin, Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100), nullable=False, default="India")
    state: Mapped[Optional[str]] = mapped_column(String(100))
    city: Mapped[Optional[str]] = mapped_column(String(100))
    locality: Mapped[Optional[str]] = mapped_column(String(150))
    postal_code: Mapped[Optional[str]] = mapped_column(String(20))

    projects: Mapped[list["Project"]] = relationship(back_populates="location")
    labour_rates: Mapped[list["LabourRate"]] = relationship(back_populates="location")
    material_prices: Mapped[list["MaterialPrice"]] = relationship(back_populates="location")


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey("locations.id"), index=True)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    project_type: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    client_name: Mapped[Optional[str]] = mapped_column(String(200))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    owner: Mapped["User"] = relationship(back_populates="projects")
    location: Mapped[Optional["Location"]] = relationship(back_populates="projects")
    site: Mapped[Optional["ProjectSite"]] = relationship(
        back_populates="project",
        uselist=False,
        cascade="all, delete-orphan",
    )
    estimates: Mapped[list["Estimate"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan",
    )


class ProjectSite(TimestampMixin, Base):
    __tablename__ = "project_sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    plot_area_sqft: Mapped[Optional[Decimal]] = mapped_column(Numeric(14, 2))
    built_up_area_sqft: Mapped[Optional[Decimal]] = mapped_column(Numeric(14, 2))
    floors: Mapped[int] = mapped_column(default=1, nullable=False)
    bedrooms: Mapped[int] = mapped_column(default=0, nullable=False)
    bathrooms: Mapped[int] = mapped_column(default=0, nullable=False)
    kitchens: Mapped[int] = mapped_column(default=1, nullable=False)
    balconies: Mapped[int] = mapped_column(default=0, nullable=False)
    parking_spaces: Mapped[int] = mapped_column(default=0, nullable=False)
    construction_type: Mapped[Optional[str]] = mapped_column(String(100))
    site_conditions: Mapped[Optional[str]] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="site")


class Estimate(TimestampMixin, Base):
    __tablename__ = "estimates"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    version: Mapped[int] = mapped_column(default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="draft", nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text)

    project: Mapped["Project"] = relationship(back_populates="estimates")
    items: Mapped[list["EstimateItem"]] = relationship(
        back_populates="estimate",
        cascade="all, delete-orphan",
    )


class Unit(TimestampMixin, Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(80), nullable=False)
    dimension: Mapped[str] = mapped_column(String(40), nullable=False)

    materials: Mapped[list["Material"]] = relationship(back_populates="default_unit")


class Material(TimestampMixin, Base):
    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(primary_key=True)
    default_unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"), nullable=False)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    specification: Mapped[Optional[str]] = mapped_column(Text)
    brand: Mapped[Optional[str]] = mapped_column(String(120))
    sku: Mapped[Optional[str]] = mapped_column(String(100))

    default_unit: Mapped["Unit"] = relationship(back_populates="materials")
    prices: Mapped[list["MaterialPrice"]] = relationship(back_populates="material")
    estimate_items: Mapped[list["EstimateItem"]] = relationship(back_populates="material")


class Supplier(TimestampMixin, Base):
    __tablename__ = "suppliers"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    supplier_type: Mapped[str] = mapped_column(String(50), nullable=False)
    website: Mapped[Optional[str]] = mapped_column(String(500))
    contact_name: Mapped[Optional[str]] = mapped_column(String(150))
    phone: Mapped[Optional[str]] = mapped_column(String(40))
    email: Mapped[Optional[str]] = mapped_column(String(320))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    prices: Mapped[list["MaterialPrice"]] = relationship(back_populates="supplier")


class PriceSource(TimestampMixin, Base):
    __tablename__ = "price_sources"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[Optional[str]] = mapped_column(String(1000))
    reliability_score: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    prices: Mapped[list["MaterialPrice"]] = relationship(back_populates="source")


class MaterialPrice(TimestampMixin, Base):
    __tablename__ = "material_prices"

    id: Mapped[int] = mapped_column(primary_key=True)

    material_id: Mapped[int] = mapped_column(
        ForeignKey("materials.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    supplier_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("suppliers.id"),
        index=True,
    )
    source_id: Mapped[int] = mapped_column(
        ForeignKey("price_sources.id"),
        nullable=False,
        index=True,
    )
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id"),
        index=True,
    )

    price: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    unit_code: Mapped[str] = mapped_column(String(30), nullable=False)

    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))

    minimum_order_quantity: Mapped[Optional[Decimal]] = mapped_column(Numeric(14, 2))
    notes: Mapped[Optional[str]] = mapped_column(Text)

    material: Mapped["Material"] = relationship(back_populates="prices")
    supplier: Mapped[Optional["Supplier"]] = relationship(back_populates="prices")
    source: Mapped["PriceSource"] = relationship(back_populates="prices")
    location: Mapped[Optional["Location"]] = relationship(back_populates="material_prices")


class EstimateItem(TimestampMixin, Base):
    __tablename__ = "estimate_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    estimate_id: Mapped[int] = mapped_column(
        ForeignKey("estimates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    material_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("materials.id"),
        index=True,
    )

    item_type: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    quantity: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    unit_code: Mapped[str] = mapped_column(String(30), nullable=False)
    unit_rate: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(16, 4), nullable=False)

    estimate: Mapped["Estimate"] = relationship(back_populates="items")
    material: Mapped[Optional["Material"]] = relationship(back_populates="estimate_items")


class LabourRate(TimestampMixin, Base):
    __tablename__ = "labour_rates"

    id: Mapped[int] = mapped_column(primary_key=True)
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id"),
        index=True,
    )

    role: Mapped[str] = mapped_column(String(100), nullable=False)
    skill_level: Mapped[Optional[str]] = mapped_column(String(50))
    rate: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR", nullable=False)
    unit_code: Mapped[str] = mapped_column(String(30), nullable=False)
    observed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    location: Mapped[Optional["Location"]] = relationship(back_populates="labour_rates")


class CostRule(TimestampMixin, Base):
    __tablename__ = "cost_rules"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    rule_type: Mapped[str] = mapped_column(String(60), nullable=False)
    value: Mapped[Decimal] = mapped_column(Numeric(14, 4), nullable=False)
    unit: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False)
    entity_id: Mapped[Optional[int]] = mapped_column()
    old_value: Mapped[Optional[str]] = mapped_column(Text)
    new_value: Mapped[Optional[str]] = mapped_column(Text)
    reason: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )