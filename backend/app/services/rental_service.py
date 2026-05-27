# 대여 비즈니스 로직 (라우터에서 호출)
from datetime import UTC, datetime, timedelta

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.rental import Rental

DEFAULT_RENTAL_DAYS = 7


def create_rental(db: Session, asset_id: int, user_id: str) -> Rental:
    asset = db.get(Asset, asset_id)
    if asset is None:
        raise ValueError("asset_not_found")
    if asset.status != "available":
        raise ValueError("asset_not_available")

    active = (
        db.query(Rental)
        .filter(Rental.asset_id == asset_id, Rental.returned_at.is_(None))
        .first()
    )
    if active is not None:
        raise ValueError("asset_already_rented")

    now = datetime.now(UTC)
    rental = Rental(
        asset_id=asset_id,
        user_id=user_id,
        started_at=now,
        due_at=now + timedelta(days=DEFAULT_RENTAL_DAYS),
    )
    db.add(rental)
    db.commit()
    db.refresh(rental)
    return rental


def list_user_rentals(db: Session, user_id: str) -> list[Rental]:
    return (
        db.query(Rental)
        .filter(Rental.user_id == user_id)
        .order_by(Rental.started_at.desc())
        .all()
    )
