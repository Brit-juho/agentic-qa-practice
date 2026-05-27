# ARCHITECTURE.md

이 프로젝트의 *지켜야 할 아키텍처 기준*. 멤버의 architecture-guardian 에이전트가 위반을 잡아낼 때 비교 대상이 된다.

## 1. 레이어 분리

```
┌───────────────┐
│   Router      │ ← FastAPI 엔드포인트, HTTP 직접 처리만
└───────┬───────┘
        ▼
┌───────────────┐
│   Service     │ ← 비즈니스 로직, 도메인 규칙
└───────┬───────┘
        ▼
┌───────────────┐
│   Repository  │ ← DB 접근만 (SQLAlchemy 쿼리)
└───────┬───────┘
        ▼
┌───────────────┐
│      DB       │
└───────────────┘
```

원칙:
- Router는 **HTTP만** 다룬다 — 입력 파싱 / 응답 직렬화 / Service 호출
- Router에 *비즈니스 로직 작성 금지* (조건문이 도메인 규칙이면 Service로)
- Service는 *Router에 직접 의존하지 않음* — 양방향 의존 금지
- Repository는 *DB 액세스만* — 도메인 결정 금지

## 2. 단일 진실 원천 (Single Source of Truth)

상태 정보는 *한 군데*만 가진다.

예시:
- ❌ `Asset.status`(available/in_use)와 `Rental.returned_at`(NULL/timestamp) **둘 다**로 "사용 중인지" 판단
- ✅ `Rental.returned_at IS NULL`만으로 판단. `Asset.status`는 *유지보수* 같은 다른 상태에만 사용

이중 상태는 *불일치*를 만든다. 한쪽만 업데이트되는 버그 발생.

## 3. DTO vs Model 구분

- **Model** (`app/models/`): DB 테이블과 1:1 매핑 (SQLAlchemy)
- **DTO/Schema** (Pydantic): API 입출력 형식

Model을 *그대로* API 응답으로 내보내지 않는다 — DTO를 거친다. 이유:
- 내부 필드 노출 방지 (예: `password_hash`)
- API 스키마와 DB 스키마의 *독립 진화*

## 4. 인증/권한 흐름

- 인증: `X-User-Id` 헤더에서 user_id 추출 (이 워크숍의 *가짜* 인증)
- 권한: Service 레이어에서 *명시적*으로 체크
  - 예: 반납 처리 전 `rental.user_id == current_user_id` 검증
- Router에서 권한 체크하지 않는다 (Service의 책임)

## 5. 트랜잭션 경계

- 한 비즈니스 작업 = 한 트랜잭션
- 트랜잭션은 *Service*에서 시작/커밋 (Router나 Repository가 아님)
- 동시성 충돌이 가능한 작업(예: 같은 장비 동시 대여)은 *낙관적 락* 또는 *DB 제약*으로 보호

## 6. 테스트 기대치

- Service 레이어는 단위 테스트로 *비즈니스 규칙*을 검증
- Router는 통합 테스트로 *HTTP 경계 + 권한 + 응답 형식*을 검증
- 엣지 케이스 (경계 시간, 권한 거부, 동시성)는 *별도* 테스트 케이스로
