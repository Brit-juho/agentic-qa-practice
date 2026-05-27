# DECISIONS.md

호스트가 직접 답하지 못한 결정들을 Claude Code가 *자동으로* 내리면서 기록한 로그. 각 항목에 *대안*과 *왜 그 선택을 했는지*를 적었다. 마음에 안 드는 결정이 있으면 이 파일을 보고 되돌릴 수 있다.

## 형식

```
### D{N} — {결정 항목}
- 선택: {선택지}
- 대안: {다른 선택지들}
- 이유: {왜 이걸 골랐는지}
- 영향 파일: {이 결정으로 영향 받은 파일들}
- 되돌리기: {바꾸려면 어디를 수정해야 하는지}
```

---

## 워크숍 디자인 결정

### D1 — 레포 이름
- 선택: `agentic-qa-practice`
- 대안: `fornerds-consensus-review`, `multi-agent-review-lab`
- 이유: 책 용어 직접 사용해서 외부 공유 가능. 호스트가 명세서에서 처음 언급한 톤과 가장 가까움.
- 영향 파일: README.md, CLAUDE.md (이름 언급된 곳)
- 되돌리기: README.md, CLAUDE.md에서 `agentic-qa-practice` 일괄 치환. 디렉토리는 그대로 사용 가능 (GitHub 레포명만 다르게 생성하면 됨).

### D2 — 멤버 보고서 PR 타겟
- 선택: 메인 레포에 직접 PR
- 대안: 각자 fork에 머지 후 링크만 공유
- 이유: 호스트가 모임 후 누적된 PR을 한 자리에서 비교 분석할 수 있음. 산출물의 핵심이 *멤버별 에이전트 카탈로그*인데, 분산되면 합성 어려움.
- 영향 파일: README.md Step 5, docs/WORKSHOP-FLOW.md
- 되돌리기: README.md Step 5의 `gh pr create --repo` 부분을 본인 fork 머지 안내로 교체.

### D3 — Cursor/기타 도구 사용자 fallback
- 선택: README에 한 단락으로 manual 절차 안내
- 대안: 아예 "Claude Code 필수"로 명시 / 별도 트랙 만들기
- 이유: 한 단락 추가 비용은 작고, 멤버 다양성에 대한 안전망. 단 fallback 사용자는 산출물(`.claude/agents/`)이 자연스럽게 안 만들어지므로 별도 가공 필요.
- 영향 파일: README.md 맨 아래
- 되돌리기: 해당 섹션 삭제.

### D4 — 작업 디렉토리
- 선택: `/Users/woosung/project/practice/fornerds_study_session5/` 직접 사용 (별도 하위 폴더 안 만듦)
- 대안: `agentic-qa-practice/` 하위 폴더 생성
- 이유: 현재 디렉토리가 비어있고 이름이 session5라 *이 디렉토리 자체가 레포*인 게 자연스러움. 하위 폴더 만들면 불필요한 nesting.
- 영향 파일: 모든 파일 위치
- 되돌리기: 모든 파일을 새 하위 폴더로 이동 (`mkdir agentic-qa-practice && mv ...`).

---

## 기술 스택 결정

### D5 — Backend DB
- 선택: SQLAlchemy + SQLite
- 대안: in-memory dict (외부 의존 없음)
- 이유: N+1 쿼리 함정이 *진짜 ORM*에서 자연스럽게 발생. 멤버가 실제 PR과 같은 감각으로 리뷰 가능. SQLite는 파일 한 개라 설치 부담 없음.
- 영향 파일: `backend/pyproject.toml`, `backend/app/db.py`, `backend/app/models/`
- 되돌리기: SQLAlchemy 제거 후 `db.py`를 dict 기반으로 재작성. 모델도 dataclass로 변경.

### D6 — Backend 인증 방식
- 선택: `X-User-Id` 헤더 기반 *가짜* 인증
- 대안: JWT / OAuth / Session
- 이유: 워크숍은 *보안 함정*을 보는 게 목적이지 인증 시스템 학습이 아님. 가짜 인증은 30줄로 끝나고 권한 우회 함정을 자연스럽게 보여줌. JWT는 100줄+ 추가 + 라이브러리 의존성.
- 영향 파일: `backend/app/auth.py`, 모든 라우터
- 되돌리기: `app/auth.py`를 JWT 구현으로 교체. 라우터에서 dependency 갱신.

### D7 — Frontend 빌더
- 선택: Vite
- 대안: Create React App, Next.js, Remix
- 이유: 가장 빠른 dev 서버, 단순한 설정. Next.js는 SSR/라우팅 등 워크숍에 불필요한 복잡도 추가. CRA는 deprecated.
- 영향 파일: `frontend/package.json`, `frontend/vite.config.ts`
- 되돌리기: Vite 제거 후 Next.js로 마이그레이션 (구조 큰 변경 필요).

### D8 — Frontend 상태 관리
- 선택: React useState/useEffect만
- 대안: Redux, Zustand, React Query
- 이유: 코드 라인 최소. React Query 같은 거 추가하면 *그것 자체 리뷰*가 필요해짐. 함정 #4 (useEffect deps 누락)는 순수 React에서 자연스러움.
- 영향 파일: `frontend/src/pages/*`
- 되돌리기: 외부 상태 라이브러리 추가 (큰 리팩토링 필요).

### D9 — Python 버전
- 선택: 3.11+
- 대안: 3.10, 3.12
- 이유: FastAPI 최신 기능 활용. 3.11이 현재(2026-05) 가장 보편적.
- 영향 파일: `backend/pyproject.toml`, README 사전 준비
- 되돌리기: pyproject.toml의 `requires-python`만 수정.

### D10 — Node 버전
- 선택: 20+
- 대안: 18, 22
- 이유: Vite 5+ 최소 요구 + LTS.
- 영향 파일: README 사전 준비
- 되돌리기: README의 버전 명시만 수정.

---

## 함정 배치 결정 (feat/return-extend 브랜치)

### D11 — 함정 #1 보안: 권한 체크 누락
- 위치: `backend/app/routers/rentals.py` `PATCH /rentals/{id}/return`
- 형태: `rental_id`만 받고 *누구의 대여인지 검증 안 함* → 남의 대여 반납 가능
- 정답: Service 레이어에서 `rental.user_id == current_user_id` 체크

### D12 — 함정 #2 보안: XSS
- 위치: `frontend/src/pages/ReturnExtend.tsx`
- 형태: 장비명을 `dangerouslySetInnerHTML`로 렌더링 → 장비명에 `<script>` 삽입 가능
- 정답: 일반 텍스트 렌더링 또는 sanitize

### D13 — 함정 #3 성능: N+1 쿼리
- 위치: `backend/app/routers/assets.py` `GET /assets?availability=true`
- 형태: 장비 리스트 가져온 후 *각 장비마다* `rental` 조회 → N+1
- 정답: `joinedload` 또는 단일 join 쿼리

### D14 — 함정 #4 성능: useEffect deps 누락
- 위치: `frontend/src/pages/MyRentals.tsx`
- 형태: `useEffect(..., [])`에 의존성 빠짐 → 페이지 진입 시만 fetch, 갱신 안 됨
- 정답: 의존성 명시 또는 refetch 트리거

### D15 — 함정 #5 테스트: 동시 대여 경합 미테스트
- 위치: `backend/tests/test_rentals.py` (해당 테스트 *부재*)
- 형태: 같은 장비를 두 사용자가 동시 대여 시도 → 한쪽만 성공해야 하는데 테스트 없음
- 정답: 동시성 테스트 추가 또는 DB 제약 검증

### D16 — 함정 #6 테스트: 반납일 초과 미테스트
- 위치: `backend/tests/test_rentals.py` (해당 테스트 *부재*)
- 형태: 반납일 지난 대여를 연장하면? 반납 처리 시 페널티? 테스트 없음
- 정답: 경계 시간 테스트 케이스 추가

### D17 — 함정 #7 아키텍처: 라우터에 비즈니스 로직
- 위치: `backend/app/routers/rentals.py` `PATCH /rentals/{id}/extend`
- 형태: 연장 가능 여부 (현재 대여 중인지, 최대 연장 횟수 등) 판단을 *라우터*에서 직접 작성
- 정답: `services/rental_service.py`로 이동

### D18 — 함정 #8 아키텍처: 상태 이중 저장
- 위치: `backend/app/models/asset.py`, `backend/app/routers/rentals.py`
- 형태: 대여 시 `Asset.status = "in_use"` *와* `Rental` 레코드 둘 다 사용. 한쪽 갱신 누락 시 불일치
- 정답: `Asset.status`는 *유지보수* 같은 시스템 상태만, 대여 여부는 `Rental.returned_at IS NULL`로 판단

---

## 함정의 *교묘함* 수준

선택: **중간 수준**.

이유: 너무 명백하면 (보안 함정 옆에 `# TODO: 권한 체크 필요` 같은 주석) 멤버 학습 효과 ↓. 너무 교묘하면 시간 부족. *실제 PR에서 자주 보이는 자연스러운 누락* 수준으로 박음.

---

## 미해결/향후 검토

이 워크숍이 끝나고 호스트가 다음 회차 또는 다음 도메인을 추가할 때 고려할 사항.

- 함정을 *9개 이상*으로 확장 시 4축 균형 재검토
- 도메인 추가 시 (예: 회의실 예약) `samples/` 같은 디렉토리로 분리
- CI/CD 통합 (책 보너스 과제) — GitHub Actions로 매 PR마다 `/consensus-review` 자동 실행

---

## 호스트가 직접 확인 권장

다음 항목들은 *자동 결정*이지만 호스트의 *팀 컨텍스트*에 따라 다를 수 있어 한 번 봐주면 좋음.

1. [D1] 레포 이름 — `agentic-qa-practice`가 정말 GitHub에 올릴 이름인가?
2. [D2] PR 타겟 — 메인 레포가 외부 공개라면 PR 누적이 어수선해 보일 수 있음. 내부 자산이면 OK.
3. [D6] 가짜 인증 — 만약 *진짜 인증*을 보여주고 싶으면 JWT로 바꾸되 코드량 ↑.
4. [D11~D18] 함정 8개의 *위치* — 너무 한 파일에 몰리면 한 리뷰어가 다 잡음. 분산 적절한지 확인.
