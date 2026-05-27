---
description: 합의 기반 코드 리뷰 — 풍부한 PR 컨텍스트로 4개 전문 리뷰어 병렬 발사 + 합의 종합. 비계획 발견 적극 유도.
argument-hint: <target-branch> (기본값 feat/return-extend)
---

# /consensus-review

Tutorial 22 *합의 기반 코드 리뷰* 패턴을 한 명령으로 굴립니다. 각 리뷰어가 *PR diff뿐 아니라 commit 메시지·프로젝트 컨벤션·관련 코드 컨텍스트*까지 받아 깊이 있는 발견을 합니다.

## 사용법

```
/consensus-review feat/return-extend
```

인자 생략 시 `feat/return-extend` 가정.

---

## 너의 임무 (Claude)

### Step 1 — 사전 점검

순서대로 확인. 빠진 게 있으면 *어떤 게 빠졌는지 정확히* 안내 후 중단.

1. 인자로 받은 브랜치(`$1`, 없으면 `feat/return-extend`)가 존재하는가 — `git rev-parse --verify $1`
2. `main` 브랜치가 존재하는가
3. `.claude/agents/` 아래 5개 모두 있는가
   - `security-reviewer.md` (호스트 샘플)
   - `consensus-synthesizer.md` (호스트 샘플)
   - `performance-analyst.md` (멤버 자작)
   - `test-coverage-reviewer.md` (멤버 자작)
   - `architecture-guardian.md` (멤버 자작)
4. `outputs/` 디렉토리가 있는가 (없으면 생성)

빠진 에이전트가 멤버 자작이면 `docs/AGENT-GUIDE.md` 와 `docs/AGENT-TEMPLATE.md` 참조 안내.

### Step 2 — PR 컨텍스트 수집 (강화)

단순 diff만 보면 *비계획 발견*이 적게 나온다. *PR 전체 컨텍스트*를 수집해서 각 리뷰어에게 전달.

```bash
# 1) 변경 통계
git diff main...$1 --stat

# 2) commit 목록 (PR의 *변경 의도*와 *발전 흐름* 파악)
git log main..$1 --pretty=format:"%h %s%n%b%n---"

# 3) 변경된 파일 목록 (status별)
git diff main...$1 --name-status

# 4) 전체 diff
git diff main...$1
```

위 4개를 변수로 저장. diff가 0이면 중단. diff가 10000줄+이면 경고만 출력하고 진행.

### Step 3 — 4개 리뷰어 병렬 발사 (풍부한 컨텍스트)

Task 도구로 4개 sub-agent를 *병렬*로 발사. **반드시 한 메시지에 4개 동시 호출**.

각 호출에 다음 형식의 풍부한 프롬프트 전달:

```
당신은 .claude/agents/{agent-name}.md 의 명세에 따라 합의 기반 코드 리뷰의
*{axis}* 관점을 담당합니다.

## 리뷰 대상 PR
브랜치: $1 → main
변경 통계: [diff stat]
변경된 파일: [name-status]

## PR의 의도와 발전 흐름 (commit 메시지)
[git log main..$1 의 모든 commit 메시지 본문 통째]

## 프로젝트 컨벤션 (반드시 참조)
- `CLAUDE.md` — 프로젝트 전반 컨텍스트
- `docs/ARCHITECTURE.md` — 지켜야 할 아키텍처 기준
- `docs/AGENT-GUIDE.md` — 합의 리뷰 패턴 가이드
- 위 파일들을 Read 도구로 직접 읽어서 컨벤션 위반을 식별하세요.

## 변경 사항 (diff)
[git diff main...$1 전체]

## 추가 컨텍스트 수집 권한
필요하면 Grep/Read로 *변경 파일과 관련된 다른 파일*도 직접 확인하세요.
예: 변경된 함수가 어디서 호출되는지, 비슷한 패턴이 다른 곳에 있는지.

## 분석 요청 — 표면적 발견을 넘어서

다음 5가지 차원을 *적극적으로* 탐색하세요:

1. **계획된 결함**: PR diff에서 명백히 잘못된 코드
2. **컨벤션 위반**: ARCHITECTURE.md 기준과 어긋나는 부분
3. **비계획 발견 (Unplanned Findings)**: 개발자가 의도하지 않았지만
   진짜 문제인 것. 예: deprecated API, 누락된 에러 처리, 코드 스멜
4. **연쇄 영향 (Cascading Impact)**: 한 곳의 결함이 다른 곳에
   미치는 영향. 예: 권한 누락이 데이터 무결성으로 번지는 경로
5. **결합 시나리오 (Combined Risks)**: 단독으론 Low지만 다른 결함과
   결합 시 Critical이 되는 것. 예: 정보 노출 + XSS = 토큰 탈취

각 발견에 *Confidence* (High/Medium/Low)를 명시. 추측이면 Low.

## 출력 형식
{axis-specific-agent}.md의 출력 명세를 따르되, 위 5가지 차원의 발견을
모두 포함하세요. *얕은 발견 5개보다 깊은 발견 3개가 낫습니다.*
```

`{axis}`는 각 리뷰어에 맞게: `보안` / `성능` / `테스트 커버리지` / `아키텍처`.

### Step 4 — 합의 종합 (강화)

4개 결과를 받은 후 `consensus-synthesizer` sub-agent 호출. 입력 프롬프트:

```
당신은 .claude/agents/consensus-synthesizer.md 명세에 따라
4개 전문 리뷰의 결과를 단일 통합 리포트로 합성합니다.

## PR 컨텍스트
[PR 메타데이터 + commit 메시지 — Step 2에서 수집한 것]

## 4개 전문 리뷰 결과
### Security Review
[보안 리뷰 결과 원본]

### Performance Review
[성능 리뷰 결과 원본]

### Test Coverage Review
[테스트 리뷰 결과 원본]

### Architecture Review
[아키텍처 리뷰 결과 원본]

## 의무 — 단순 합산 금지

4가지 의무를 *명시적으로* 수행한 흔적이 출력에 보여야 합니다.

1. **중복 병합**: 같은 이슈의 다른 표현 → 하나로 (공동 발견자 기록)
2. **충돌 해결**: 리뷰어 간 권고 모순 → 명시적 판단 + 근거
3. **우선순위 재평가**: Critical/High/Medium/Low 통합 기준
4. **차단 여부 라벨**: 모든 이슈에 Blocking/Non-blocking

## 추가 요구

5. **비계획 발견 별도 섹션**: 4개 리뷰가 잡은 *비계획 발견*은
   "Unplanned Findings"로 별도 강조. 호스트가 이를 보고 *워크숍 가치*
   를 측정.
6. **결합 시나리오**: 두 발견이 결합 시 심각도가 올라가는 경우
   "Combined Risks" 섹션에 명시.
7. **이 PR의 한 줄 위험 요약**: Executive Summary 최상단에
   "이 PR이 머지되면 *가장 큰 위험*은: ..." 한 줄.
```

### Step 5 — 결과 저장

```bash
GIT_USER=$(git config user.name | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
OUTPUT_PATH="outputs/unified-review-${GIT_USER}-${TIMESTAMP}.md"
```

Write 도구로 통합 리포트를 `$OUTPUT_PATH`에 저장.

### Step 6 — 보고

```
✓ 합의 기반 코드 리뷰 완료

대상: main...$1
변경: N파일, M줄, K commits
리뷰어: 4 (security / performance / test / architecture)
종합: consensus-synthesizer

발견 요약:
- 총: N개 (Critical X / High Y / Medium Z / Low W)
- 차단: M개 (Blocking)
- 비계획 발견: K개 (호스트 의도 외)

결과: outputs/unified-review-<user>-<timestamp>.md

다음:
1. 결과 정독: cat outputs/unified-review-*.md
2. PR 브랜치 생성: git checkout -b review/$GIT_USER
3. 자기 .claude/agents/ + 결과를 commit → 자기 fork push → 메인 레포 PR
```

---

## 엣지 케이스

### 멤버 자작 에이전트 빠짐
어떤 게 빠졌는지 명확히 안내 + `docs/AGENT-TEMPLATE.md` 참조. 중단.

### `consensus-synthesizer` 빠짐 (멤버가 실수로 지움)
호스트 샘플 복원 안내:
```
git checkout main -- .claude/agents/consensus-synthesizer.md
```

### diff가 너무 큼 (10000줄+)
경고 출력 + 그래도 진행 (멤버 판단).

### sub-agent 호출 실패
실패한 리뷰만 재시도. 3회 연속 실패 시 부분 결과로 진행하고
*어떤 리뷰가 빠졌는지* 종합 리포트에 명시.

### git 사용자 이름 미설정
`GIT_USER`가 비어있으면 `anonymous-<timestamp>`로 fallback.

---

## 왜 이 명령이 단순 4번 던지기보다 강력한가

1. **commit 메시지를 컨텍스트로** — 개발자의 *의도*와 어긋난 코드를 잡아냄
2. **프로젝트 컨벤션 자동 참조** — `ARCHITECTURE.md` 위반을 명시적으로 감지
3. **5가지 분석 차원** — 표면적 발견(diff)을 넘어 *비계획 발견*과
   *결합 시나리오*까지
4. **Confidence 표시** — Low confidence 발견을 별도 분류해서
   *과잉 경보* 방지
5. **합의 단계의 4+3 의무** — 충돌 해결, 우선순위, 차단 라벨에
   더해 *비계획 발견 강조*와 *한 줄 위험 요약*
