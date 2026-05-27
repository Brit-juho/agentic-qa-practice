# prompts/

멤버가 *복사해서 쓰는* 프롬프트 모음. *읽고 학습하는 문서*가 아닌 *재료*.

## 파일

| 파일 | 용도 |
|---|---|
| [`book-prompts.md`](book-prompts.md) | 책 *에이전틱 코딩* Tutorial 22 (p311~314) 6단계 프롬프트 원문 — 본인 에이전트 만들 때 타이핑 시간 절약용 복사 시작점. 끝에 도전 과제 한 단락. |

## 사용법

```bash
# 본인 에이전트 작성 시
cat prompts/book-prompts.md
# → 필요한 단계 프롬프트 복사
# → .claude/agents/<name>.md 에 frontmatter 추가 후 본인 컨텍스트로 진화
```

## 관련 문서

- [`docs/AGENT-GUIDE.md`](../docs/AGENT-GUIDE.md) — 책 4축 + 합의 패턴 개념
- [`docs/AGENT-TEMPLATE.md`](../docs/AGENT-TEMPLATE.md) — Custom Agent frontmatter 형식 + 좋은 예/나쁜 예
- [`.claude/agents/security-reviewer.md`](../.claude/agents/security-reviewer.md) — 책 프롬프트가 *진화한 결과* 예시 (호스트 샘플)

## 핵심 원칙

**책 프롬프트는 *출발점*이지 *종착점*이 아님.** 그대로 복붙하면 함정 12개 중 6~8개만 잡힘. 본인 도메인 경험을 더 녹여 baseline을 넘어서세요.
