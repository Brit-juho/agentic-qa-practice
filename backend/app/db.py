# SQLAlchemy 세션과 시드 데이터를 관리
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

DATABASE_URL = "sqlite:///./rental.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models.asset import Asset
    from app.models.rental import Rental  # noqa: F401

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Asset).count() > 0:
            return

        seed_assets = [
            Asset(name="MacBook Pro 14", asset_type="laptop", status="available"),
            Asset(name="Dell 27 4K Monitor", asset_type="monitor", status="available"),
            Asset(name="Logitech MX Master 3S", asset_type="mouse", status="available"),
            Asset(name="HHKB Pro Hybrid", asset_type="keyboard", status="available"),
            Asset(name="Sony WH-1000XM5", asset_type="headphone", status="maintenance"),
        ]
        db.add_all(seed_assets)
        db.commit()
    finally:
        db.close()
