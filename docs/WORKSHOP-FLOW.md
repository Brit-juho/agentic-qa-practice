# WORKSHOP-FLOW.md

모임 당일 호스트와 멤버의 *세부 흐름*. 운영용.

## 호스트 사회자 큐 카드

### 시작 직전 (5분)
- 멤버 환경 확인 (Claude Code 실행, gh 인증 완료, 레포 fork 완료)
- 막힌 사람 손 들기 → 빠르게 해결
- 화면 공유로 본인의 fork 한 번 시연

### 0–5분: 도메인 + PR 설명
- 도메인: 사내 장비 대여 (장비 조회 + 기본 대여 + *반납/연장 추가 PR*)
- 리뷰 대상: `feat/return-extend` 브랜치
- 함정 수: 12개 (4축 각 3개, 위치/종류 비공개)
- 난이도: 중-중상 (일부 함정은 React/Python 깊은 지식 필요)

### 5–10분: PR diff 같이 훑기
- 화면 공유로 `git diff main...feat/return-extend` 같이 보기
- 멤버 각자 *직관적으로 의심스러운 부분* 메모 (이건 자기 가설)

### 10–25분: 에이전트 작성 (15분)
- AGENT-GUIDE.md, AGENT-TEMPLATE.md 한 번 띄워둠
- 호스트는 *질문만 받음* — 답 알려주지 않음
- 25분 시점에 **종료 시그널** → 미완 상태라도 다음 단계로

### 25–35분: 합의 리뷰 실행 + 정독
- `/consensus-review feat/return-extend` 일제히 실행
- 결과 정독 → 자기 가설과 비교

### 35–40분: PR 생성 (5분)
- 명령어는 README에 그대로 있음
- 막힌 사람 호스트가 직접 도움

### 모임 종료 후
- 호스트는 누적된 PR들 정리, 다음 주 모임에서 *공유 토론*

## 멤버 흐름 (자기용)

```
fork → clone → checkout feat/return-extend → diff 확인 →
.claude/agents/ 에 3개 작성 →
/consensus-review feat/return-extend →
outputs/ 확인 →
review/<이름> 브랜치 → commit → push → PR
```

## 위험 상황 대응

| 상황 | 대응 |
|---|---|
| 멤버 환경 셋업 30분 잡아먹음 | 미리 정해둔 *공유 fork*에서 동작 보고 토론만 |
| 에이전트 작성이 너무 어려워함 | AGENT-TEMPLATE.md의 "좋은 예" 복붙 → 일부만 수정하도록 안내 |
| 시간 안에 PR까지 못 감 | `outputs/`만 commit해서 push, PR은 모임 후 |
| `/consensus-review` 실패 | 책 p311의 4단계 프롬프트 수동 4번 던지기로 fallback |

## 모임 후 호스트 작업

1. 누적된 PR 5~10개 한 자리에 모음
2. 각 PR의 `.claude/agents/` 비교
   - 같은 역할에서 *공통적으로 잡힌 검사 기준*
   - *한 명만 잡은* 좋은 검사 기준
   - 누구도 안 잡은 *누락된* 검사 기준
3. 위 3가지를 모아 `docs/FORNERDS-STANDARD.md` 작성
4. 다음 주 모임에서 공유 → 팀 표준 확정
