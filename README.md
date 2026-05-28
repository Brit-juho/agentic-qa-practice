# agentic-qa-practice

포너즈 북클럽 5회차(에이전틱 코딩 13~14장) **합의 기반 코드 리뷰 워크숍** 레포.

멤버가 _자기 스타일로_ 전문 리뷰어 에이전트를 작성하고, 합의 종합으로 통합 리뷰 리포트를 만든 뒤 PR로 제출한다. 모임 후 호스트가 멤버 PR들을 모아 *포너즈 표준 에이전트*를 합성한다.

---

## 워크숍 한 장 요약

```
[호스트가 미리 준비함]
- main 브랜치: 안전한 MVP (장비 조회 + 기본 대여)
- feat/return-extend 브랜치: 반납/연장 기능 추가 PR (의도된 결함 8개 포함)
- 샘플 에이전트 2개: security-reviewer, consensus-synthesizer
- 슬래시 커맨드: /consensus-review

[멤버 모임 당일 흐름 — 40분]
1. 이 레포 Fork & clone
2. feat/return-extend 체크아웃 → PR diff 확인 (feat/return-extend → main)
3. 자기 작업 브랜치 생성 (feat/review-<본인이름>)
4. 자기 에이전트 3개 작성 (performance-analyst, test-coverage-reviewer, architecture-guardian)
5. /consensus-review feat/return-extend 실행 (에이전트 빠지면 경고 후 중단)
6. outputs/unified-review-<이름>.md 생성
7. commit → 자기 fork push → 메인 레포에 PR  ← 여기까지 1차
8. (시간 여유 시) 2차 — 호스트가 공유한 함정 답안지로 자가 채점

[모임 후]
호스트가 누적된 PR들에서 좋은 패턴 추출 → 포너즈 표준 에이전트 카탈로그 작성
```

---

## 사전 준비

- **Claude Code** 최신 버전 ([설치 가이드](https://docs.claude.com/claude-code))
- **Python 3.11+** + **uv** ([설치](https://docs.astral.sh/uv/getting-started/installation/) — `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Node 20+** + **npm**
- **GitHub CLI (`gh`)** — fork 및 PR 생성에 사용
- **make** (macOS/Linux 기본 포함, Windows는 wsl 권장)

설치 확인:

```bash
make check-tools
```

> Cursor/Codex 등 다른 도구 사용자는 본 README 맨 아래 _"Cursor 사용자 fallback"_ 섹션 참조.

## Quick Start (한 명령)

```bash
git clone <레포-URL>
cd agentic-qa-practice
make install          # 백엔드(uv sync) + 프론트엔드(npm install)

# 두 터미널에서 따로 실행
make backend          # http://localhost:8000
make frontend         # http://localhost:5173
```

전체 명령 보기: `make help`

---

## Step 1 — Fork & Clone

```bash
# 메인 레포 fork
gh repo fork <메인레포-URL> --clone --remote

# 또는 GitHub UI에서 fork 후
git clone https://github.com/<your-id>/agentic-qa-practice.git
cd agentic-qa-practice

# 메인 레포를 upstream으로 추가 (PR 보낼 곳)
git remote add upstream <메인레포-URL>
git fetch upstream
```

---

## Step 2 — 리뷰 대상 PR diff 확인

```bash
# 트랩 브랜치 체크아웃
git checkout feat/return-extend

# diff 한 번 훑어보기
git diff main...feat/return-extend --stat
git diff main...feat/return-extend
```

읽으면서 _"여기 문제 있어 보이는데?"_ 부분을 머릿속에 기록. 자기 에이전트가 그 문제들을 잡아내야 한다.

가설을 메모했으면 트랩 브랜치 위에서 *자기 작업 브랜치*를 만든다. 이후 모든 작업(에이전트 작성 · 리뷰 · PR)은 이 브랜치에서 진행한다.

```bash
git checkout -b feat/review-<본인이름>   # 예: feat/review-woosung
```

> 트랩 브랜치(`feat/return-extend`)에서 분기하므로 이 브랜치엔 트랩 PR 내용 + (이후 추가할) 자기 에이전트만 얹힌다. 그래서 리뷰는 `feat/return-extend`가 아니라 _이 브랜치(`feat/review-<이름>`)를 그대로_ 대상으로 돌린다 (Step 4). 코드 변경은 트랩 PR과 동일하고 추가분은 `.claude/agents/`뿐이라 트랩 검증엔 영향이 없다.

---

## Step 3 — 자기 에이전트 3개 작성

호스트가 만들어둔 2개:

- `.claude/agents/security-reviewer.md` — 보안 리뷰어 (참고 샘플)
- `.claude/agents/consensus-synthesizer.md` — 합의 종합자 (통제 변수: 그대로 사용)

멤버가 만들 3개:

- `.claude/agents/performance-analyst.md`
- `.claude/agents/test-coverage-reviewer.md`
- `.claude/agents/architecture-guardian.md`

작성 가이드: [`docs/AGENT-GUIDE.md`](docs/AGENT-GUIDE.md) 와 [`docs/AGENT-TEMPLATE.md`](docs/AGENT-TEMPLATE.md) 참조.

핵심 원칙: *자기 도메인 경험*을 녹여라. 책 그대로 베끼지 말 것. 결과물의 다양성이 산출물의 가치.

---

## Step 4 — 합의 리뷰 실행

```bash
# 지금 자기 작업 브랜치에 있어야 함 (Step 2에서 생성)
git branch --show-current   # → feat/review-<본인이름>

# Claude Code 진입
claude

# 인자 없이 실행 — 현재 브랜치(feat/review-<이름>)를 자동으로 리뷰 대상으로
> /consensus-review
```

> 자기 작업 브랜치에서 그대로 리뷰한다. 인자를 생략하면 현재 브랜치(`feat/review-<이름>`)가 대상이 되고, 이 브랜치는 트랩 PR(`feat/return-extend`) 위에 자기 에이전트만 얹힌 상태라 트랩 검증에 그대로 쓸 수 있다.

내부 동작: 0. _사전 점검_ — `.claude/agents/` 에 5개(샘플 2 + 자작 3)가 모두 있는지 확인.
하나라도 빠지면 **무엇이 빠졌는지 안내하고 중단** (리뷰 진행 안 함). 다 있으면 진행.

1. 리뷰 대상 브랜치 해석 — 인자로 받은 `feat/return-extend` 사용 (인자 생략 시 현재 브랜치 자동 감지)
2. `git diff main...<대상>` + commit log + 파일 통계 수집
3. `.claude/agents/` 안의 4개 리뷰어 병렬 발사 (Task 도구)
   - 각 리뷰어에 PR 컨텍스트 + 프로젝트 컨벤션(CLAUDE.md, ARCHITECTURE.md) 전달
4. 4개 결과를 합의 종합자에게 전달 (충돌 해결 + 우선순위 + 결합 시나리오 + 한 줄 위험 요약)
5. `outputs/unified-review-<git-user>-<timestamp>.md` 로 저장 (기존 파일 _덮어쓰지 않음_)

> **에이전트 부족 시**: 자작 3개(`performance-analyst` / `test-coverage-reviewer` / `architecture-guardian`)
> 중 하나라도 없으면 커맨드가 경고를 출력하고 멈춘다. `docs/AGENT-TEMPLATE.md`를 참고해
> 빠진 에이전트를 채운 뒤 다시 실행. (실수로 `consensus-synthesizer`를 지웠다면
> `git checkout main -- .claude/agents/consensus-synthesizer.md`로 복원)

---

## Step 5 — 보고서 PR 생성

```bash
# 이미 feat/review-<본인이름> 브랜치에 있음 (Step 2에서 생성)
git branch --show-current   # → feat/review-<본인이름>

# 에이전트 + 리뷰 결과 commit
git add .claude/agents/performance-analyst.md
git add .claude/agents/test-coverage-reviewer.md
git add .claude/agents/architecture-guardian.md
git add outputs/unified-review-*.md
git commit -m "review: 합의 기반 코드 리뷰 — <본인 이름>"

# 자기 fork로 push
git push origin feat/review-<본인이름>

# 메인 레포에 PR
gh pr create --repo <메인레포> \
  --base main \
  --title "review: <본인 이름>의 합의 리뷰" \
  --body "Tutorial 22 워크숍 결과물. 에이전트 3개 + 통합 리뷰 리포트 포함."
```

여기까지가 **1차**. 시간이 남으면 아래 *2차*로.

---

## 시간 안배 (40분 기준)

| 시간    | 활동                        |
| ------- | --------------------------- |
| 0–5분   | Fork & clone, README 훑기   |
| 5–10분  | PR diff 읽고 함정 위치 추측 |
| 10–25분 | 에이전트 3개 작성           |
| 25–30분 | `/consensus-review` 실행    |
| 30–35분 | 결과 정독, 자기 가설과 비교 |
| 35–40분 | 보고서 PR 생성              |

25분에 에이전트 작성이 안 끝났으면 *지금 있는 만큼*으로 실행. 완벽한 에이전트보다 *제출된 에이전트*가 산출물.

> **2차(자가 채점)** 는 위 40분 밖. 1차 PR을 다 낸 사람부터 시간 여유가 있을 때 진행한다 (아래 _2차_ 섹션 참조).

---

## 🎭 Playwright MCP로 검증 (선택)

이 PR엔 **코드만 읽어선 안 보이고 _실행해야 보이는 버그_** 도 포함돼 있습니다. 자기 에이전트가 잡지 못한 부분을 _실제 동작_ 으로 확인하고 싶다면:

```bash
# 1. 백엔드 + 프론트엔드 실행 (두 터미널)
make backend
make frontend

# 2. Claude Code에서 Playwright MCP 활용
> http://localhost:5173 열고 다음 시나리오들 검증해줘:
>   - 장비 빌리고 반납/연장 시도 (라벨 vs 실제 동작 일치?)
>   - 빠른 연속 클릭 시 동작
>   - 모든 대여를 반납했을 때 화면 안내
>   - PATCH /rentals/{id}/extend 에 비정상 값 전송 시 (음수 등)
```

코드 리뷰가 _책상 위 검증_ 이라면, Playwright는 _실행 검증_. 둘이 잡는 영역이 다릅니다 — 합의 리뷰 리포트가 _어디까지 잡았는지_ 자가 채점해보세요.

> 호스트가 Playwright 테스트 파일을 제공하지 않는 이유: _스포일러_ (어떤 시나리오를 테스트하는지가 곧 함정 힌트). 멤버 스스로 시나리오 설계해보세요.

---

## 🥈 2차 — 자가 채점 (시간 여유 시)

1차에서 만든 통합 리뷰 리포트가 _실제로 몇 개의 함정을 잡았는지_ 답안지와 대조해 채점하는 단계. 점수 그 자체보다 **내 에이전트가 어떤 종류의 문제에 약한지** 알아내는 게 목적이다.

### 흐름

1. **1차 PR 제출 완료** — `feat/review-<이름>` 브랜치에서 PR을 만든 상태. `outputs/unified-review-<이름>.md` 가 있어야 한다.
2. **호스트가 함정 답안지 공개** — 1차를 _블라인드로_ 끝낸 뒤, 호스트가 **Notion으로 함정 정의(카테고리 + 검출 방법)** 를 공유한다. 1차 전엔 절대 공개하지 않는다 (= 스포일러).
3. **Claude에게 채점 요청** — 자기 리포트와 답안지를 함께 주고 *대조표*를 만들게 한다.
4. **같은 브랜치에 추가 commit → push** — _별도 브랜치를 만들지 않는다._ 1차에서 PR을 만든 `feat/review-<이름>` 브랜치 그대로, 채점 결과를 commit·push 하면 **기존 PR이 자동으로 업데이트**된다.

> 답안지는 호스트만 가진 채점 기준표(`TRAP-INVENTORY.md`, 레포엔 `.gitignore` 처리)에서 나온다. 멤버는 모임 중 Notion으로 받은 내용만 사용한다.

### 채점 프롬프트 예시

Claude Code에서 이렇게 던진다 (답안지는 호스트가 준 내용을 그대로 붙여넣기).

```
내 합의 리뷰 리포트(outputs/unified-review-<이름>.md)와
아래 "함정 답안지"를 대조해서 채점표를 만들어줘.

- 답안지의 카테고리별로 [내가 잡은 것 / 놓친 것] 표로 정리
- 잡은 함정은 내 리포트의 어느 발견이 대응되는지 인용
- 놓친 함정은 왜 못 잡았는지 한 줄 추정
  (에이전트 축 부재 / 코드만 봐서 / 깊이 부족 / 실행 검증 안 함 중)
- 마지막에 카테고리별 점수와 총점, 그리고 "내 에이전트의 약한 축" 한 줄 요약

[여기에 호스트가 Notion으로 준 함정 답안지 붙여넣기]
```

### 결과 제출 — 같은 브랜치에 추가 commit

별도 브랜치를 새로 만들지 않는다. 1차에서 PR을 만든 그 브랜치에 그대로 있는 상태에서 채점표를 저장하고 push 하면 기존 PR에 커밋이 얹힌다.

```bash
# 1차에서 PR 만든 브랜치 그대로 (새 브랜치 X)
git branch --show-current   # → feat/review-<본인이름>

git add outputs/scorecard-<본인이름>.md     # Claude가 만든 채점표 저장본
git commit -m "review: 2차 자가 채점 결과 — <본인 이름>"
git push origin feat/review-<본인이름>       # 기존 PR에 자동 반영
```

### 채점에서 보는 것

- _4축_(보안 · 성능 · 테스트 · 아키텍처)이 균형 있게 잡았는가 — 한 축에 쏠리지 않았는지
- 코드 리뷰로는 안 보이고 _실행(Playwright)으로만_ 드러나는 함정을 인지했는가
- _비계획 발견_(호스트가 안 박았지만 진짜 문제) 을 얼마나 건졌는가 — 에이전트 꼼꼼함의 지표

> 핵심은 점수가 아니라 _놓친 패턴_. "내 에이전트가 이런 종류에 약하다"를 알면 다음 워크숍에서 그 축을 보강할 수 있다. 채점표가 1차 PR에 같이 들어가니 모임 후 토론거리가 된다.

---

## 자주 막히는 곳 FAQ

**Q. 슬래시 커맨드가 안 보여요**  
A. Claude Code를 레포 루트에서 실행하세요. `.claude/commands/consensus-review.md` 이 인식되어야 합니다.

**Q. 에이전트가 너무 길어져요**  
A. 30~80줄이 적정. 100줄 넘으면 *역할이 너무 넓다*는 신호. 쪼개거나 줄이세요.

**Q. `/consensus-review` 실행 중 에이전트 부족 에러**  
A. `.claude/agents/` 아래에 5개(샘플 2 + 자작 3) 모두 있어야 합니다. 파일명 확인.

**Q. 합의 종합자도 직접 만들고 싶어요**  
A. 워크숍 통제 변수라 호스트 버전 사용 권장. 다만 본인 fork에서 변형해보는 건 OK — 그 경우 *비교 토론거리*가 됩니다.

**Q. backend/frontend 실제로 안 돌려도 되나요?**  
A. 리뷰는 *코드*만 봅니다. 실행 불필요. 다만 환경 세팅에 관심 있으면 `backend/README.md`, `frontend/README.md` 참조.

---

## Cursor 사용자 fallback

Claude Code 외 도구(Cursor / Codex 등) 사용자는 슬래시 커맨드가 동작 안 합니다. 대신:

1. `.claude/agents/*.md` 파일 5개의 내용을 직접 읽어 각각 *별도 프롬프트*로 던지기 (보안 → 성능 → 테스트 → 아키텍처)
2. 4개 결과를 모아 `.claude/agents/consensus-synthesizer.md` 내용으로 한 번 더 던지기
3. 결과를 `outputs/unified-review-<이름>.md`로 저장
4. 이후 Step 5와 동일

---

## 디렉토리 안내

```
agentic-qa-practice/
├── .claude/         # Custom Agents + Slash Commands
├── backend/         # FastAPI (장비 대여 API)
├── frontend/        # React + TypeScript (대여 UI)
├── docs/            # 에이전트 가이드, 아키텍처
└── outputs/         # 멤버 리뷰 리포트 저장
```

---

## 라이센스

MIT
