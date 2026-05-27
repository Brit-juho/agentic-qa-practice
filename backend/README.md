# backend — 장비 대여 API

FastAPI + SQLAlchemy + SQLite. 의존성은 `uv`로 관리.

## 실행

레포 루트에서 `make` 사용 권장:

```bash
make install        # uv sync
make backend        # dev 서버 (port 8000)
make test-backend   # pytest
```

직접 실행하려면:

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

## 테스트

```bash
uv run pytest
```

`tests/conftest.py`가 in-memory SQLite + 시드 데이터를 fixture로 제공.

## API 한눈에

| Method | Path | 설명 | 인증 |
|---|---|---|---|
| GET | `/assets` | 장비 목록 | - |
| GET | `/assets/{id}` | 장비 상세 | - |
| POST | `/rentals` | 새 대여 | `X-User-Id` 헤더 필수 |
| GET | `/rentals/mine` | 내 대여 목록 | `X-User-Id` 헤더 필수 |

> `feat/return-extend` 브랜치엔 반납/연장/availability 엔드포인트가 추가됩니다.

## 인증

`X-User-Id: <username>` 헤더로 *가짜 인증*. 워크숍 단순화를 위함.

## 의존성 관리

- 런타임 deps → `[project].dependencies` (pyproject.toml)
- 개발 deps → `[dependency-groups].dev` (PEP 735)
- 잠금 → `uv.lock` (git commit됨)

새 패키지 추가:
```bash
uv add <package>           # 런타임
uv add --dev <package>     # 개발
```
