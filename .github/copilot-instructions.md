# GitHub Copilot Instructions

이 파일은 이 저장소에서 GitHub Copilot / Copilot Chat이 따라야 할 규약입니다.

## Repository purpose

- Microsoft Build 2026의 주요 세션을 **고객·아키텍트 관점**에서 정리하는 노트 모음.
- 사이트는 MkDocs Material 기반 GitHub Pages 로 자동 배포됨 (`hellices/microsoft-build-2026`).

## File layout (must follow)

```
docs/
├── index.md                      # 사이트 홈 (세션 인덱스)
├── contributing.md               # 작성 규약
├── sessions/
│   ├── _TEMPLATE.md              # 세션 템플릿 (수정 금지, 복사해서 사용)
│   ├── BRK000-example-session.md # 작성 예시 (참고용, 수정 가능)
│   └── <SESSION_ID>-<kebab-slug>.md   # 세션 1개 = 파일 1개
└── themes/
    ├── _TEMPLATE.md
    └── <topic>.md                # 주제별 큐레이션
```

- 모든 콘텐츠는 `docs/` 안에 위치. 루트의 `README.md` 는 GitHub 표시용이며 사이트 빌드 대상이 아님.
- 세션 ID 예: `KEY01`, `BRK226`, `DEM330`, `ODSP907`, `DEM368-R1` (R1 같은 리비전 표기 유지).
- 슬러그는 소문자·하이픈만, 관사(a/the) 생략.
- 예시 파일: [`docs/sessions/BRK000-example-session.md`](../docs/sessions/BRK000-example-session.md)

## When creating a new session

1. `docs/sessions/_TEMPLATE.md` 를 복사해 새 파일 생성.
2. Frontmatter를 모두 채우거나, 모르는 필드는 **빈 채로 두고 키는 남김** (필드 삭제 금지).
3. `_TEMPLATE.md` 의 헤더 순서·이름은 변경하지 않음. 내용 없으면 빈 채로 두기.
4. `docs/index.md` 의 해당 토픽 표에 한 줄 추가하고 상태 이모지 갱신:
   - `🔜` 예정 · `⏳` 작성 중 (`draft`/`review`) · `✅` 완료 (`done`)
5. `mkdocs.yml` 의 `nav` 트리에도 한 줄 추가 (경로는 `docs/` 기준 상대경로).

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

기본 순서 (일반 BRK/DEM 세션):

1. `## TL;DR` — 한두 문장
2. `## Top highlights` — 키노트/하이라이트 성 세션에서 정말 중요한 3~5개 항목 (`### N. 제목` + 1~2문장 요약). 일반 세션에서는 생략 가능.
3. `## Why it matters` — 고객 관점, 불릿 2~4개
4. `## Key announcements` — 표 (항목 / 상태 / 날짜 / 비고)
5. `## Session summary` — 섹션별 (`### 1.`, `### 2.` ...)
6. `## Demo highlights` — `⏱️ MM:SS — <name>: <one-liner>`
7. `## Architecture / Diagram` — 다이어그램 (아래 규칙 참고)
8. `## Code & samples` — 핵심 스니펫
9. `## Caveats / Open questions` — 미확정 사항
10. `## Resources` — Session / Slides / GitHub / Docs
11. `## Notes` — 내부 메모 (고객 배포 시 제거 가능)

### 섹션 적용 규칙

- 일반 세션 (BRK/DEM 등): 내용이 없으면 섹션을 비워두기 — 섹션 자체는 유지.
- **키노트 및 패널/요약성 세션**: 다음 섹션은 세션 성격에 맞지 않으면 **삭제 가능** — 억지로 비워두지 말 것.
  - `## Demo highlights` — 데모가 없는 키노트
  - `## Code & samples` — 코드 스니펫이 없는 세션
  - `## Resources` 안의 `💻 GitHub` 항목 — 공식 GitHub 저장소가 없는 세션 (다른 Resources 항목은 유지)
- `## Top highlights`는 정보 밀도가 매우 높은 키노트에서 권장. TL;DR 한 줄로 부족한 "이 세션에서 진짜 기억해야 할 것" 을 3~5개로 상단에 짚어줌.

## Diagrams (Excalidraw + PNG)

- 다이어그램은 **Copilot이 `.excalidraw` JSON 파일로 직접 작성**하고, 사용자는 해당 파일을 VS Code Excalidraw 에디터(`pomdtr.excalidraw-editor`)에서 열어 동일 이름으로 PNG export 만 수행.
- 폴더 규약:
  - 세션 파일: `docs/sessions/<SESSION_ID>-<slug>.md`
  - 다이어그램 폴더: `docs/sessions/<SESSION_ID>-<slug>/`
  - 다이어그램 파일: `<descriptive-name>.excalidraw` + 동일 basename `<descriptive-name>.png` (둘 다 소문자·하이픈)
- 노트에서 참조하는 방식 (PNG 만 참조):

  ```markdown
  ![Azure Boost offload architecture](BRK226-inside-azure-innovations/azure-boost-offload.png)
  ```

- Copilot이 새 세션 노트를 만들 때:
  1. 본문에 위 형식으로 PNG 참조를 적어둠 (mermaid 사용 금지 — 별도 지시가 없으면).
  2. 같은 폴더에 **각 PNG와 동일한 basename의 `.excalidraw` JSON 파일을 직접 생성**. 다이어그램이 여러 개면 다이어그램 수만큼 `.excalidraw` 파일 생성. README 파일은 만들지 않음.
  3. 다이어그램이 많거나 좌표 계산이 복잡하면 `tools/gen_<session>_diagrams.py` 같은 일회성 생성 스크립트를 만들어 일괄 생성해도 됨 (참고 예: `tools/gen_brk226_diagrams.py`). 스크립트는 유지해 두어 좌표/색상 수정 시 재실행 가능하게 함.
- Excalidraw JSON 최소 스키마:
  - 최상위: `{ "type": "excalidraw", "version": 2, "source": "...", "elements": [...], "appState": { "gridSize": null, "viewBackgroundColor": "#ffffff" }, "files": {} }`
  - 각 element는 `id, type, x, y, width, height, angle, strokeColor, backgroundColor, fillStyle, strokeWidth, strokeStyle, roughness, opacity, groupIds, frameId, roundness, seed, version, versionNonce, isDeleted, boundElements, updated, link, locked` 필드를 가짐. type별 추가 필드 (text → `text, fontSize, fontFamily, textAlign, verticalAlign, baseline, containerId, originalText, lineHeight`; arrow → `points, lastCommittedPoint, startBinding, endBinding, startArrowhead, endArrowhead`).
- 사용자가 동일한 basename으로 PNG export 만 하면 본문 참조가 자동 표시됨.
- 예외: 단순 흐름/시퀀스 등 텍스트 다이어그램이 더 적절하다고 사용자가 명시한 경우에만 mermaid 사용.

## When creating a new theme page

- `docs/themes/_TEMPLATE.md` 복사 → `docs/themes/<topic>.md`.
- Related sessions 섹션에는 실제 작성된 세션 노트만 링크.

## Things Copilot should NOT do

- `docs/sessions/_TEMPLATE.md`, `docs/themes/_TEMPLATE.md` 의 구조를 수정.
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
