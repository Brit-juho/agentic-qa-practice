---
description: 합의 기반 코드 리뷰 — 4개 전문 리뷰어 병렬 발사 + 합의 종합 보고서 생성
argument-hint: <target-branch> (기본값 feat/return-extend)
---

# /consensus-review

Tutorial 22 *합의 기반 코드 리뷰* 패턴을 한 명령으로 굴립니다.

## 사용법

```
/consensus-review feat/return-extend
```

인자를 생략하면 `feat/return-extend` 가정.

## 너의 임무 (Claude)

### Step 1 — 사전 점검

다음을 *순서대로* 확인하고, 빠진 게 있으면 사용자에게 *명확히* 안내한 뒤 중단.

1. 인자로 받은 브랜치(`$1`, 없으면 `feat/return-extend`)가 존재하는가 — `git rev-parse --verify $1`
2. `main` 브랜치가 존재하는가
3. `.claude/agents/` 아래에 다음 5개가 모두 있는가
   - `security-reviewer.md` (호스트 샘플)
   - `consensus-synthesizer.md` (호스트 샘플)
   - `performance-analyst.md` (멤버 자작)
   - `test-coverage-reviewer.md` (멤버 자작)
   - `architecture-guardian.md` (멤버 자작)
4. `outputs/` 디렉토리가 있는가 (없으면 생성)

빠진 에이전트가 있으면 *어떤 게 빠졌는지* 정확히 안내. 멤버 자작 3개 중 빠진 게 있다면 `docs/AGENT-GUIDE.md`와 `docs/AGENT-TEMPLATE.md` 참조 안내.

### Step 2 — diff 계산

```bash
git diff main...$1 > /tmp/consensus-review-diff.txt
wc -l /tmp/consensus-review-diff.txt
```

diff 크기를 사용자에게 보고 (변경된 파일 목록 + 줄 수). diff가 0이면 중단.

### Step 3 — 4개 리뷰어 병렬 발사

Task 도구로 4개 sub-agent를 *병렬*로 발사한다. *반드시 한 번의 메시지로 4개 동시 호출*.

각 호출의 입력은 다음 형식:

```
다음은 리뷰 대상 diff다. main...$1 사이의 변경 사항.

[diff 내용 통째 첨부]

당신은 .claude/agents/{agent-name}.md 의 명세에 따라 리뷰를 작성한다.
출력은 그 명세의 출력 형식 그대로.
```

4개 sub-agent:
- `security-reviewer`
- `performance-analyst`
- `test-coverage-reviewer`
- `architecture-guardian`

### Step 4 — 합의 종합

4개 결과를 받은 후 `consensus-synthesizer` sub-agent를 호출한다.

입력:
```
다음은 4개 전문 리뷰의 결과다.

## Security Review
[보안 리뷰 결과]

## Performance Review
[성능 리뷰 결과]

## Test Coverage Review
[테스트 리뷰 결과]

## Architecture Review
[아키텍처 리뷰 결과]

당신은 .claude/agents/consensus-synthesizer.md 의 명세에 따라 통합 리포트를 작성한다.
출력은 그 명세의 출력 형식 그대로.
```

### Step 5 — 결과 저장

종합 결과를 다음 경로에 저장.

```bash
GIT_USER=$(git config user.name | tr ' ' '-' | tr '[:upper:]' '[:lower:]')
TIMESTAMP=$(date -u +%Y%m%d-%H%M%S)
OUTPUT_PATH="outputs/unified-review-${GIT_USER}-${TIMESTAMP}.md"
```

Write 도구로 통합 리포트를 `$OUTPUT_PATH`에 저장.

### Step 6 — 보고

사용자에게 다음을 출력:

```
✓ 합의 기반 코드 리뷰 완료

대상: main...$1
변경: N파일, M줄
리뷰어: 4 (security / performance / test / architecture)
결과: outputs/unified-review-<user>-<timestamp>.md

다음 단계 (자동 안내):
1. 결과 정독: cat outputs/unified-review-*.md
2. PR 브랜치 생성: git checkout -b review/$GIT_USER
3. add → commit → push → gh pr create (README Step 5 참조)
```

## 엣지 케이스

### 멤버 자작 에이전트 빠짐
어떤 자작 에이전트가 빠졌는지 명확히 표시하고 `docs/AGENT-TEMPLATE.md` 참조 안내. 중단.

### `consensus-synthesizer` 빠짐 (멤버가 실수로 지움)
호스트 샘플을 복원하라고 안내. 또는 다음 명령 안내:
```
git checkout main -- .claude/agents/consensus-synthesizer.md
```

### diff가 너무 큼 (10000줄+)
경고 출력. 그래도 진행은 함 (멤버 판단에 맡김).

### sub-agent 호출 실패
실패한 리뷰만 재시도. 3회 연속 실패 시 부분 결과로 진행하고 *어떤 리뷰가 빠졌는지* 종합 리포트에 명시.
