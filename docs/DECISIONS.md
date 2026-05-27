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

선택: **중-중상 사이** (D31 참조).

기존 #1~#8은 *중간 수준*에서 박았으나 일부(#5/#6/#8)는 암묵적으로 중상. 추가 #9~#12는 *중상 수준*으로 박음. 평균은 *중-중상 사이*.

---

## 구현 중 추가 결정

### D19 — Frontend 디자인
- 선택: inline styles (외부 CSS 없음)
- 대안: CSS modules, Tailwind, styled-components
- 이유: 워크숍 코드는 *리뷰 대상*이지 *디자인 학습*이 아님. inline style이 최소 의존성.
- 영향 파일: `frontend/src/**/*.tsx`
- 되돌리기: CSS 파일 추가 후 className 사용으로 마이그레이션.

### D20 — Frontend 라우팅
- 선택: react-router-dom v6
- 대안: TanStack Router, 라우팅 없음
- 이유: React 생태계 표준. 멤버 모두 익숙.
- 영향 파일: `frontend/package.json`, `App.tsx`, `main.tsx`
- 되돌리기: 라우팅 제거 후 conditional rendering.

### D21 — 가짜 인증 자동 셋팅
- 선택: 페이지 진입 시 `localStorage.userId = 'alice'` 자동 셋팅
- 대안: 명시적 로그인 UI / 환경변수
- 이유: 워크숍 단순화. 멤버가 *인증*에 시간 안 씀.
- 영향 파일: `frontend/src/main.tsx`
- 되돌리기: 해당 코드 제거 + 로그인 페이지 추가.

### D22 — SQLite 파일 위치
- 선택: `backend/rental.db` (gitignore 처리됨)
- 대안: in-memory만 / `/tmp/`
- 이유: 멤버가 dev 서버 실행 시 데이터 영속. 시드는 init_db에서 자동.
- 영향 파일: `backend/app/db.py`, `.gitignore`
- 되돌리기: `DATABASE_URL`을 `sqlite:///:memory:`로 변경.

### D23 — 함정 #8 (이중 상태) 구체 구현
- 선택: `return_rental`에서 `rental.returned_at` 갱신 + `asset.status = "available"` 갱신 *둘 다* 실행
- 대안: Asset에 별도 status enum 추가하고 그쪽도 갱신
- 이유: 가장 자연스럽고 멤버가 *왜 이게 문제인지* 직관적으로 봄. 한쪽 실패시 영구 불일치.
- 영향 파일: `backend/app/routers/rentals.py` (return_rental)
- 정답 방향: `asset.status`는 *유지보수* 같은 시스템 상태만, 대여 여부는 `Rental.returned_at`로만 판단

### D24 — 함정 #7 (라우터 비즈니스 로직) 구체 구현
- 선택: `extend_rental`의 최대 연장 기간 계산 + 검증 *전부* router 함수 안에서
- 대안: services에 함수만 만들어두고 호출
- 이유: 실제 PR에서 흔히 보이는 "급해서 라우터에 박은" 패턴. 자연스러움.
- 영향 파일: `backend/app/routers/rentals.py` (extend_rental)
- 정답 방향: `services/rental_service.py`에 `extend_rental` 추가하고 router에서 호출

### D25 — 함정 #3 (N+1) 구체 구현
- 선택: `list_assets_with_availability`에서 장비 루프 안에서 `Rental` 별도 쿼리
- 대안: `joinedload` 사용, 단일 LEFT JOIN
- 이유: 가장 흔한 ORM 안티패턴. 성능 리뷰어가 *명백히* 잡아야 함.
- 영향 파일: `backend/app/routers/assets.py`
- 정답 방향: `selectinload(Asset.rentals)` 또는 명시적 JOIN

### D26 — 테스트 누락 함정의 *형태*
- 선택: return/extend의 *해피 패스만* 테스트하고 엣지 케이스 부재
- 대안: 테스트 파일 자체를 비움 / 잘못된 단언 작성
- 이유: 비어있으면 너무 명백 / 잘못된 단언은 *다른 종류의 함정*. 누락이 가장 현실적.
- 영향 파일: `backend/tests/test_rentals.py`
- 정답 방향: 동시성, 권한, 경계 시간(overdue), 최대 연장 초과 케이스 추가

---

## 함정 #9~#12 (FE 균형 + 난이도 중상 업그레이드)

호스트 피드백으로 FE 함정 4개 추가 (총 8 → 12). 4축 각 3개로 균형.

### D27 — 함정 #9 보안: 에러 로깅에 민감 정보 노출
- 위치: `frontend/src/api/client.ts` `handleError`
- 형태: 에러 시 `console.error`로 status / headers 전체 / URL / 응답 body / **localStorage.userId** 출력. XSS와 결합 시 토큰 탈취 경로.
- 난이도: 중상 (친절한 진단 로깅처럼 보임)
- 정답 방향: 메시지만 출력 + 민감 키 마스킹 + 프로덕션에선 로깅 레벨 조절

### D28 — 함정 #10 성능: 매 렌더 비싼 연산 + React 안티패턴
- 위치: `frontend/src/pages/AssetList.tsx`
- 형태: (1) `visible` 배열을 매 렌더마다 `filter().filter().sort()` 신규 생성, (2) `actions: { rent: () => ..., refresh: () => ... }` 매번 새 객체+함수, (3) `meta: { filters: { typeFilter, search } }` 매번 새 객체, (4) `key={index}` 사용
- 난이도: 중상 (React 깊은 지식 필요)
- 정답 방향: `useMemo`로 visible 캐싱, `useCallback`으로 함수 안정화, `key={asset.id}`, 자식 `React.memo`

### D29 — 함정 #11 테스트: 인프라만 있고 테스트 0개
- 위치: `frontend/tests/setup.ts` + `frontend/vitest.config.ts` (있음). `frontend/tests/*.test.tsx` (없음)
- 형태: vitest + testing-library 설치 완료, 글로벌 셋업도 완료. 하지만 *.test.tsx 파일 0개. 커밋 메시지 "테스트 파일은 별도 PR에서" — 영원히 안 옴.
- 난이도: 중상 (부재를 알아채야 함)
- 정답 방향: 최소 AssetList / MyRentals / ReturnExtend 각 happy path 테스트 추가

### D30 — 함정 #12 아키텍처: API 클라이언트에 비즈니스 로직 + 우회 fetch
- 위치: `frontend/src/api/client.ts` + `frontend/src/pages/ReturnExtend.tsx`
- 형태: (1) `fetchAssets`가 `retired` 필터 + 한글 정렬 *내부 수행* (도메인 로직), (2) `fetchActiveAssetsForUser`는 client.ts가 다른 client.ts 함수를 합성하며 권한 판단까지, (3) `ReturnExtend.tsx`는 client.ts 우회해서 `fetch(BASE + ...)` 직접 호출
- 난이도: 중상 (정답이 한 가지 아님)
- 정답 방향: client.ts는 *원시 API 호출만*, 비즈니스 로직은 별도 모듈 또는 selector. ReturnExtend.tsx의 누락된 `returnRental`/`extendRental`을 client.ts에 추가하고 사용

### D31 — 난이도 정책: 중상으로 업그레이드
- 선택: #9~#12는 *중상 수준*. 기존 #1~#8 중 #5/#6/#8은 *암묵적 중상*. 나머지 #1~#4/#7는 *중*.
- 대안: 전체 중상으로 통일 (난이도 ↑ 시간 부족 위험)
- 이유: 평균 *중-중상* 사이가 40분 안에 완주 가능한 한계. 모든 함정이 중상이면 시간 안에 못 끝남.
- 영향 파일: 모든 함정 파일
- 되돌리기: 함정을 더 명백하게 (주석/TODO 추가) 또는 더 교묘하게 (더 깊이 숨김)

### D32 — 균형: BE 6 + FE 6 (4축 각 3개)
- 선택: 함정 분포를 *축별로 균형*하게 + *영역별로 균형*하게
- 대안: BE 위주 (현실적이지만 FE 리뷰어 일거리 적음)
- 이유: 멤버가 어떤 분야 전문가든 *자기 도메인의 함정*을 잡을 거리 보장
- 영향 파일: `frontend/*` 전부 + `backend/*` 일부
- 분포 표:

| 축 | Backend | Frontend |
|---|---|---|
| 보안 | #1 권한 | #2 XSS, #9 로깅 노출 |
| 성능 | #3 N+1 | #4 useEffect, #10 비싼 렌더 |
| 테스트 | #5 동시성, #6 overdue | #11 테스트 0개 |
| 아키텍처 | #7 라우터 로직, #8 이중 상태 | #12 API 클라이언트 |

`rentals.py`에 #1/#7/#8 3개 몰림은 *대여* 도메인의 핵심 라우터라 자연스러움. 다른 함정들은 분산됨.

---

## 인프라 결정 (D33~)

### D33 — Python 패키지 관리: uv
- 선택: `uv` (Astral) + `[dependency-groups]` (PEP 735)
- 대안: pip + venv (기존), poetry, hatch
- 이유: 멤버 환경 세팅 30초 → 3초. `uv.lock`으로 재현성 보장. pyproject.toml은 표준 `[project]` 유지해서 pip 사용자도 호환.
- 영향 파일: `backend/pyproject.toml`, `backend/uv.lock`, `backend/README.md`, `README.md` Quick Start
- 되돌리기: `uv.lock` 삭제 + `dependency-groups`를 `optional-dependencies`로 변경 + 안내 문구 수정

### D34 — Makefile로 진입점 통합
- 선택: 루트에 `Makefile` 추가 (help/install/backend/frontend/test/clean)
- 대안: 셸 스크립트, npm scripts at root, just(justfile)
- 이유: Make는 macOS/Linux 기본 포함. 한 명령 `make install`로 두 스택 의존성 설치. `make help` 자동 문서화.
- 영향 파일: `Makefile`, `README.md`, `backend/README.md`
- 되돌리기: `Makefile` 삭제 + README에서 직접 명령 안내

### D35 — uv.lock commit 포함
- 선택: `uv.lock`을 git에 commit
- 대안: gitignore 처리
- 이유: 멤버마다 의존성 버전 통일 → 환경 차이로 인한 에러 회피. 워크숍 재현성 ↑.
- 영향 파일: `.gitignore` (uv.lock 제외 안 함), `backend/uv.lock`
- 되돌리기: `.gitignore`에 `uv.lock` 추가

### D36 — 테스트 fixture SQLite StaticPool
- 선택: `conftest.py`에서 `poolclass=StaticPool` 사용
- 대안: 파일 기반 SQLite (tempfile)
- 이유: in-memory SQLite는 연결마다 별도 DB → fixture에서 생성한 테이블을 라우터가 못 봄. StaticPool로 단일 연결 공유.
- 영향 파일: `backend/tests/conftest.py`
- 되돌리기: `poolclass` 제거 후 tempfile 기반으로 전환

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
