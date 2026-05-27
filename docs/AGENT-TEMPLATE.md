# AGENT-TEMPLATE.md

자기 에이전트 만들 때 복붙 시작점. Claude Code Custom Agent 형식.

## Frontmatter 필수 필드

```markdown
---
name: performance-analyst
description: 코드 변경에서 성능 병목과 비효율을 찾는 전문 리뷰어. /consensus-review가 자동 호출.
tools: Read, Grep, Bash
model: opus
---
```

- `name`: 파일명과 동일 (kebab-case). 슬래시 커맨드가 이 이름으로 호출
- `description`: 한 줄. 자동 라우팅 판단 근거
- `tools`: 에이전트가 쓸 수 있는 도구. 리뷰어는 보통 `Read, Grep, Bash` 정도
- `model`: `opus`(깊이) 또는 `sonnet`(속도)

## 본문 구조 (추천)

```markdown
# 역할
당신은 [도메인]의 전문가입니다. [핵심 책임 1줄].

# 검사 기준
다음 항목들을 *우선순위 순*으로 점검합니다.

1. [기준 1] — [무엇을 보고 어떻게 판단하는지]
2. [기준 2]
3. ...

# 입력
호출자가 다음을 제공합니다:
- 변경된 코드 (`git diff main...feat/return-extend` 결과)
- 관련 컨텍스트 (선택)

# 출력 형식
다음 Markdown 구조로 응답합니다:

## 발견 사항

### [#N] {제목}
- 위치: `파일경로:줄번호`
- 심각도: Critical / High / Medium / Low
- 이슈: (2~3줄 설명)
- 수정 방향: (구체적 제안)
- 차단 여부: Yes / No

## 요약
(이슈 N개, 그중 차단 M개)
```

## 좋은 예 (보안 리뷰어 발췌)

```markdown
# 역할
당신은 OWASP Top 10과 한국 웹 서비스 보안 사례에 정통한 보안 전문가입니다.

# 검사 기준
1. 인증 우회 — 권한 체크 누락, 본인 데이터만 접근 가능한가
2. 인젝션 — SQL/NoSQL/Command/LDAP 인젝션 여부
3. XSS — 사용자 입력의 HTML/JS 렌더링 시 escape 누락
...
```

## 나쁜 예 (왜 안 좋은지)

```markdown
# 역할
모든 보안 문제와 성능 문제를 찾는 만능 리뷰어입니다.
```

→ 역할이 *너무 넓음*. 합의 종합 단계에서 다른 리뷰어와 *중복/충돌*만 늘어난다.

```markdown
# 검사 기준
1. 보안을 확인합니다.
2. 좋은 코드인지 봅니다.
```

→ 기준이 *모호함*. Claude가 무엇을 봐야 할지 모름.

## 책 인용 (참고용)

책 p311 1단계 프롬프트의 원형:
> "이 코드 변경 사항에 대한 멀티에이전트 리뷰 시스템을 설정해 줘. 네 가지 전문 리뷰어를 정의해 줘. (1) 보안 전문가..."

본 워크숍에서는 이 프롬프트를 *멤버 각자의 도메인 컨텍스트*로 다듬어 작성한다.

## 디렉토리에 저장

```
.claude/agents/{name}.md
```

저장 후 Claude Code를 재시작하면 자동 인식.
