# backend — 장비 대여 API

FastAPI + SQLAlchemy + SQLite.

## 실행

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

## 테스트

```bash
pytest
```

## API 한눈에

| Method | Path | 설명 | 인증 |
|---|---|---|---|
| GET | `/assets` | 장비 목록 | - |
| GET | `/assets/{id}` | 장비 상세 | - |
| POST | `/rentals` | 새 대여 | `X-User-Id` 헤더 필수 |
| GET | `/rentals/mine` | 내 대여 목록 | `X-User-Id` 헤더 필수 |

> `feat/return-extend` 브랜치엔 반납/연장 엔드포인트가 추가됩니다.

## 인증

`X-User-Id: <username>` 헤더로 *가짜 인증*. 워크숍 단순화를 위함.
