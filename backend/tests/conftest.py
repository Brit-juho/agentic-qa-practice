# 테스트용 in-memory SQLite + TestClient fixture
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base, get_db
from app.main import app

TEST_DB_URL = "sqlite:///:memory:"


@pytest.fixture
def client():
    engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
    TestSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    from app.models.asset import Asset

    seed = TestSession()
    seed.add_all(
        [
            Asset(name="MacBook Pro 14", asset_type="laptop", status="available"),
            Asset(name="Dell Monitor", asset_type="monitor", status="available"),
            Asset(name="Sony Headphone", asset_type="headphone", status="maintenance"),
        ]
    )
    seed.commit()
    seed.close()

    yield TestClient(app)

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
