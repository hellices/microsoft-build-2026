# GitHub Copilot Instructions

이 파일은 이 저장소에서 GitHub Copilot / Copilot Chat이 따라야 할 규약입니다.

## Repository purpose

- Microsoft Build 2026의 주요 세션을 **고객·아키텍트 관점**에서 정리하는 노트 모음.
- 사이트는 MkDocs Material 기반 GitHub Pages 로 자동 배포됨 (`hellices/microsoft-build-2026`).

## File layout (must follow)

```
sessions/<SESSION_ID>-<kebab-slug>.md   # 세션 1개 = 파일 1개
themes/<topic>.md                       # 주제별 큐레이션
sessions/_TEMPLATE.md                   # 세션 템플릿 (수정 금지, 복사해서 사용)
themes/_TEMPLATE.md                     # 주제 템플릿 (수정 금지, 복사해서 사용)
```

- 세션 ID 예: `KEY01`, `BRK226`, `DEM330`, `ODSP907`, `DEM368-R1` (R1 같은 리비전 표기 유지).
- 슬러그는 소문자·하이픈만, 관사(a/the) 생략.
- 예시 파일: [`sessions/BRK000-example-session.md`](../sessions/BRK000-example-session.md)

## When creating a new session

1. `sessions/_TEMPLATE.md` 를 복사해 새 파일 생성.
2. Frontmatter를 모두 채우거나, 모르는 필드는 **빈 채로 두고 키는 남김** (필드 삭제 금지).
3. `_TEMPLATE.md` 의 헤더 순서·이름은 변경하지 않음. 내용 없으면 빈 채로 두기.
4. `README.md` 의 해당 토픽 표에 한 줄 추가하고 상태 이모지 갱신:
   - `🔜` 예정 · `⏳` 작성 중 (`draft`/`review`) · `✅` 완료 (`done`)
5. `mkdocs.yml` 의 `nav` 트리에도 한 줄 추가.

## Writing rules

- **언어**: 본문은 한국어. 제품·기능명·SDK명 등 고유명사는 영어 원문 유지 (번역 금지).
- **톤**: 마케팅 형용사 금지 (revolutionary, game-changing, seamless 등). 사실 기반으로.
- **상태 표기**: GA / Public Preview / Private Preview / Roadmap 중 선택, **확인 일자 함께 기록**.
  - GA/Preview 일자는 추측 금지. 확인할 수 없으면 빈 칸으로 두고 caveat에 기록.
- **링크**: 실제 존재하는 URL만. `build.microsoft.com/en-US/sessions/<ID>?source=sessions` 패턴은 안전하게 사용 가능. 그 외 추측 URL 생성 금지.
- **이모지**: 섹션 헤더와 Resources 리스트에만 제한적으로 사용. 본문엔 자제.

## Frontmatter schema

```yaml
session_id: BRK000           # 필수
title: ""                    # 필수, 원문 그대로
speakers: []                 # 알 수 있으면 "Name (Role, Org)" 형식
track: ""                    # Keynote | Agents | Observability | Data | Security | ...
level:                       # 100 | 200 | 300 | 400
duration_min:                # 정수
tags: []                     # 소문자, 하이픈
status: draft                # draft | review | done (필수)
last_updated: YYYY-MM-DD     # 필수
```

## Required sections in every session note

순서 고정:

1. `## TL;DR` — 한두 문장
2. `## Why it matters` — 고객 관점, 불릿 2~4개
3. `## Key announcements` — 표 (항목 / 상태 / 날짜 / 비고)
4. `## Session summary` — 섹션별 (`### 1.`, `### 2.` ...)
5. `## Demo highlights` — `⏱️ MM:SS — <name>: <one-liner>`
6. `## Architecture / Diagram` — mermaid 또는 이미지 (선택)
7. `## Code & samples` — 핵심 스니펫 (선택)
8. `## Caveats / Open questions` — 미확정 사항
9. `## Customer takeaways` — `- [ ]` 체크리스트
10. `## Resources` — Session / Slides / GitHub / Docs
11. `## Notes` — 내부 메모 (고객 배포 시 제거 가능)

내용이 없으면 섹션을 비워둘 것 — 섹션 자체를 삭제하지 않음.

## When creating a new theme page

- `themes/_TEMPLATE.md` 복사 → `themes/<topic>.md`.
- Related sessions 섹션에는 실제 작성된 세션 노트만 링크.

## Things Copilot should NOT do

- `sessions/_TEMPLATE.md`, `themes/_TEMPLATE.md` 의 구조를 수정.
- `mkdocs.yml` 의 `theme` / `plugins` / `markdown_extensions` 블록을 임의 변경.
- 발표자 이메일·내부 URL·NDA 콘텐츠 포함.
- 영어 본문으로 전환하거나 마케팅 톤으로 다시 쓰기.
- 존재 확인되지 않은 URL/제품명/기능명 생성.

## Local preview

```bash
pip install mkdocs-material
mkdocs serve   # http://127.0.0.1:8000
```

푸시하면 `.github/workflows/deploy-site.yml` 이 자동으로 GitHub Pages 배포.
