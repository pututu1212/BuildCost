from sqlalchemy import select

from backend.app.db.base import (
    CostRule,
    LabourRate,
    Location,
    Material,
    MaterialPrice,
    PriceSource,
    Unit,
    User,
)

from backend.app.db.session import SessionLocal


def seed():
    db = SessionLocal()
    
    try:
        # ---------------------------------------------------------
        # Development User
        # ---------------------------------------------------------
        user = db.scalar(
            select(User).where(User.email == "dev@buildcost.local")
        )

        if not user:
            db.add(
                User(
                    name="BuildCost Developer",
                    email="dev@buildcost.local",
                    is_active=True,
                )
            )

        db.flush()
        # ---------------------------------------------------------
        # Units
        # ---------------------------------------------------------
        units = [
            ("kg", "Kilogram", "mass"),
            ("bag", "Bag", "count"),
            ("m3", "Cubic Metre", "volume"),
            ("sqft", "Square Foot", "area"),
            ("piece", "Piece", "count"),
            ("litre", "Litre", "volume"),
            ("hour", "Hour", "time"),
            ("day", "Day", "time"),
        ]

        for code, name, dimension in units:
            if not db.scalar(select(Unit).where(Unit.code == code)):
                db.add(
                    Unit(
                        code=code,
                        name=name,
                        dimension=dimension,
                    )
                )

        db.flush()

        # ---------------------------------------------------------
        # Location
        # ---------------------------------------------------------
        location = db.scalar(
            select(Location).where(
                Location.city == "Bengaluru",
                Location.state == "Karnataka",
            )
        )

        if not location:
            location = Location(
                country="India",
                state="Karnataka",
                city="Bengaluru",
            )
            db.add(location)

        db.flush()

        # ---------------------------------------------------------
        # Price Sources
        # ---------------------------------------------------------
        sources = [
            ("User Entered", "manual"),
            ("Manufacturer", "manufacturer"),
            ("Supplier", "supplier"),
            ("IndiaMART", "marketplace"),
        ]

        for name, source_type in sources:
            if not db.scalar(
                select(PriceSource).where(PriceSource.name == name)
            ):
                db.add(
                    PriceSource(
                        name=name,
                        source_type=source_type,
                    )
                )

        db.flush()

        # ---------------------------------------------------------
        # Materials
        # ---------------------------------------------------------
        materials = [
            ("OPC 53 Cement", "Cement", "50 kg bag", "bag"),
            ("TMT Steel 12mm", "Steel", "12mm reinforcement bar", "kg"),
            ("M-Sand", "Aggregate", "Manufactured sand", "m3"),
            ("20mm Aggregate", "Aggregate", "20mm coarse aggregate", "m3"),
            ("AAC Block", "Masonry", "Standard AAC block", "piece"),
        ]

        for name, category, specification, unit_code in materials:
            if not db.scalar(
                select(Material).where(Material.name == name)
            ):
                unit = db.scalar(
                    select(Unit).where(Unit.code == unit_code)
                )

                db.add(
                    Material(
                        name=name,
                        category=category,
                        specification=specification,
                        default_unit_id=unit.id,
                    )
                )

        db.flush()

        # ---------------------------------------------------------
        # Labour Rates
        # ---------------------------------------------------------
        labour = [
            ("Mason", "skilled", 900),
            ("Helper", "unskilled", 650),
            ("Electrician", "skilled", 1000),
            ("Plumber", "skilled", 1000),
            ("Painter", "skilled", 900),
        ]

        for role, skill_level, rate in labour:
            if not db.scalar(
                select(LabourRate).where(
                    LabourRate.role == role,
                    LabourRate.location_id == location.id,
                )
            ):
                db.add(
                    LabourRate(
                        role=role,
                        skill_level=skill_level,
                        rate=rate,
                        currency="INR",
                        unit_code="day",
                        location_id=location.id,
                    )
                )

        # ---------------------------------------------------------
        # Cost Rules
        # ---------------------------------------------------------
        rules = [
            ("Material Wastage", "percentage", 5, "%"),
            ("Contingency", "percentage", 5, "%"),
            ("Contractor Overhead", "percentage", 10, "%"),
        ]

        for name, rule_type, value, unit in rules:
            if not db.scalar(
                select(CostRule).where(CostRule.name == name)
            ):
                db.add(
                    CostRule(
                        name=name,
                        rule_type=rule_type,
                        value=value,
                        unit=unit,
                    )
                )

        db.flush()

        # ---------------------------------------------------------
        # Material Prices
        # ---------------------------------------------------------
        supplier = db.scalar(
            select(PriceSource).where(
                PriceSource.name == "Supplier"
            )
        )

        price_data = [
            ("OPC 53 Cement", 420, "bag"),
            ("TMT Steel 12mm", 68, "kg"),
            ("M-Sand", 1800, "m3"),
            ("20mm Aggregate", 1600, "m3"),
            ("AAC Block", 55, "piece"),
        ]

        for material_name, price, unit_code in price_data:
            material = db.scalar(
                select(Material).where(
                    Material.name == material_name
                )
            )

            existing_price = db.scalar(
                select(MaterialPrice).where(
                    MaterialPrice.material_id == material.id,
                    MaterialPrice.location_id == location.id,
                    MaterialPrice.source_id == supplier.id,
                )
            )

            if not existing_price:
                db.add(
                    MaterialPrice(
                        material_id=material.id,
                        supplier_id=None,
                        source_id=supplier.id,
                        location_id=location.id,
                        price=price,
                        currency="INR",
                        unit_code=unit_code,
                        notes="Initial seed price for development",
                    )
                )

        db.commit()

        print("BuildCost seed completed successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()