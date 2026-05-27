# 대여 라우터 (HTTP 입출력만; 비즈니스 로직은 services로 위임)
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.auth import current_user
from app.db import get_db
from app.services import rental_service

router = APIRouter(prefix="/rentals", tags=["rentals"])


class RentalCreate(BaseModel):
    asset_id: int


class RentalOut(BaseModel):
    id: int
    asset_id: int
    user_id: str
    started_at: datetime
    due_at: datetime
    returned_at: datetime | None

    class Config:
        from_attributes = True


@router.post("", response_model=RentalOut, status_code=status.HTTP_201_CREATED)
def create_rental(
    payload: RentalCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(current_user),
) -> RentalOut:
    try:
        rental = rental_service.create_rental(db, payload.asset_id, user_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    return rental  # type: ignore[return-value]


@router.get("/mine", response_model=list[RentalOut])
def list_my_rentals(
    db: Session = Depends(get_db),
    user_id: str = Depends(current_user),
) -> list[RentalOut]:
    return rental_service.list_user_rentals(db, user_id)  # type: ignore[return-value]
