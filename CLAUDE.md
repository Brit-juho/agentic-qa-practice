# CLAUDE.md

이 레포는 **포너즈 북클럽 5회차 합의 기반 코드 리뷰 워크숍**용입니다.

## 스택
- Backend: FastAPI + SQLAlchemy + SQLite
- Frontend: React + TypeScript + Vite

## 워크숍 컨텍스트

`feat/return-extend` 브랜치엔 **의도된 결함이 박혀 있습니다**. 이는 멤버들이 자작 리뷰어 에이전트로 합의 기반 리뷰를 연습하기 위한 자료입니다.

함정의 *종류*나 *위치*는 이 파일에 절대 적지 않습니다 — 멤버 학습을 위해.

## 사용

```
/consensus-review feat/return-extend
```

`.claude/agents/` 안의 5개 에이전트(샘플 2 + 멤버 자작 3)를 병렬 발사하고 합의 종합 리포트를 `outputs/`에 저장합니다.

## 멤버 작성 가이드
- `docs/AGENT-GUIDE.md` — 책 4축 + 합의 패턴 설명
- `docs/AGENT-TEMPLATE.md` — 에이전트 작성 템플릿
- `docs/WORKSHOP-FLOW.md` — 모임 당일 상세 흐름
- `docs/ARCHITECTURE.md` — 프로젝트 아키텍처 기준
