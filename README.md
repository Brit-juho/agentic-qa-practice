# agentic-qa-practice

포너즈 북클럽 5회차(에이전틱 코딩 13~14장) **합의 기반 코드 리뷰 워크숍** 레포.

멤버가 *자기 스타일로* 전문 리뷰어 에이전트를 작성하고, 합의 종합으로 통합 리뷰 리포트를 만든 뒤 PR로 제출한다. 모임 후 호스트가 멤버 PR들을 모아 *포너즈 표준 에이전트*를 합성한다.

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
2. PR diff 확인 (feat/return-extend → main)
3. 자기 에이전트 3개 작성 (performance-analyst, test-coverage-reviewer, architecture-guardian)
4. /consensus-review feat/return-extend 실행
5. outputs/unified-review-<이름>.md 생성
6. review/<이름> 브랜치로 commit → 자기 fork push → 메인 레포에 PR

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

> Cursor/Codex 등 다른 도구 사용자는 본 README 맨 아래 *"Cursor 사용자 fallback"* 섹션 참조.

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

읽으면서 *"여기 문제 있어 보이는데?"* 부분을 머릿속에 기록. 자기 에이전트가 그 문제들을 잡아내야 한다.

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
# 트랩 브랜치에 체크아웃돼 있어야 함 (Step 2)
git branch --show-current   # → feat/return-extend 확인

# Claude Code 진입
claude

# 인자 없이 슬래시 커맨드 한 번 (현재 브랜치 자동 감지)
> /consensus-review

# 또는 명시적으로
> /consensus-review feat/return-extend
```

내부 동작:
1. *현재 브랜치* 자동 감지 (`git branch --show-current`) → 인자로 받았으면 그것 사용
2. `git diff main...<현재브랜치>` + commit log + 파일 통계 수집
3. `.claude/agents/` 안의 4개 리뷰어 병렬 발사 (Task 도구)
   - 각 리뷰어에 PR 컨텍스트 + 프로젝트 컨벤션(CLAUDE.md, ARCHITECTURE.md) 전달
4. 4개 결과를 합의 종합자에게 전달 (충돌 해결 + 우선순위 + 결합 시나리오 + 한 줄 위험 요약)
5. `outputs/unified-review-<git-user>-<timestamp>.md` 로 저장 (기존 파일 *덮어쓰지 않음*)

---

## Step 5 — 보고서 PR 생성

```bash
git checkout -b review/$(git config user.name | tr ' ' '-')

# 에이전트 + 리뷰 결과 commit
git add .claude/agents/performance-analyst.md
git add .claude/agents/test-coverage-reviewer.md
git add .claude/agents/architecture-guardian.md
git add outputs/unified-review-*.md
git commit -m "review: 합의 기반 코드 리뷰 — <본인 이름>"

# 자기 fork로 push
git push origin review/<본인이름>

# 메인 레포에 PR
gh pr create --repo <메인레포> \
  --base main \
  --title "review: <본인 이름>의 합의 리뷰" \
  --body "Tutorial 22 워크숍 결과물. 에이전트 3개 + 통합 리뷰 리포트 포함."
```

---

## 시간 안배 (40분 기준)

| 시간 | 활동 |
|---|---|
| 0–5분 | Fork & clone, README 훑기 |
| 5–10분 | PR diff 읽고 함정 위치 추측 |
| 10–25분 | 에이전트 3개 작성 |
| 25–30분 | `/consensus-review` 실행 |
| 30–35분 | 결과 정독, 자기 가설과 비교 |
| 35–40분 | 보고서 PR 생성 |

25분에 에이전트 작성이 안 끝났으면 *지금 있는 만큼*으로 실행. 완벽한 에이전트보다 *제출된 에이전트*가 산출물.

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
