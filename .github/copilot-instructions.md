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
session_type: breakout       # keynote | breakout | demo | panel | lab | lightning | announcement
title: ""                    # 필수, 원문 그대로
speakers: []                 # 알 수 있으면 "Name (Role, Org)" 형식
track: ""                    # Keynote | Agents | Observability | Data | Security | ...
level:                       # 100 | 200 | 300 | 400
duration_min:                # 정수
tags: []                     # 소문자, 하이픈
status: draft                # draft | review | done (필수)
last_updated: YYYY-MM-DD     # 필수
```

## Session note structure

세션 노트는 6 카테고리로 묶인 섹션을 사용합니다. 각 섹션에는 **포함 조건**이 정해져 있어 무조건 비워 두지 않고, 해당 없으면 통째 삭제할 수 있습니다.

| # | 카테고리 | 섹션 | 조건 |
|---|---|---|---|
| 1 | **Summary** | `## TL;DR` | 필수 |
|   |   | `## Top highlights` | 해당 시 — 키노트·정보 밀도 높은 세션 |
| 2 | **Context** | `## Why it matters` | 필수 |
|   |   | `## Customer scenarios` | 권장 — 떠오르는 실제 시나리오가 있을 때 |
| 3 | **Announcements** | `## Key announcements` (표) | 해당 시 — 발표 1건 이상 |
| 4 | **Deep dive** | `## Session summary` | 권장 — 일반 BRK/DEM에서 발표 흐름 |
|   |   | `## Architecture` | 해당 시 — 다이어그램·구조 설명 |
|   |   | `## Demo highlights` | 해당 시 — 데모가 있을 때 |
|   |   | `## Code & samples` | 해당 시 — 핵심 코드 등장 |
| 5 | **Assessment** | `## Caveats & open questions` | 권장 — 미확정 사항이 있을 때 |
| 6 | **References** | `## Resources` | 필수 — 최소 Session 링크 |
|   |   | `## Related sessions` | 권장 — 연관 세션 |
|   |   | `## Notes` | 권장 — 내부 메모, 공개 전 정리 |

순서는 위 표의 카테고리·섹션 순서를 따릅니다. 섹션 헤딩 이름은 변경하지 않습니다 (조건에 따라 통째 삭제만 함).

### 조건별 처리 원칙

- **필수**: 어떤 세션이든 항상 포함하고 채움.
- **권장**: 내용이 있으면 채우고, 정말로 비어 있을 때만 섹션을 통째 삭제.
- **해당 시**: 세션 성격에 맞을 때만 포함. 없으면 통째 삭제 (빈 채로 두지 않음).

### session_type별 권장 조합

| session_type | 핵심 섹션 |
|---|---|
| `keynote`      | TL;DR · **Top highlights** · Why it matters · Key announcements · Resources |
| `breakout`     | TL;DR · Why it matters · Customer scenarios · Key announcements · **Session summary** · Architecture · Demo · Code · Caveats · Resources |
| `demo`         | TL;DR · Why it matters · **Demo highlights** · **Code & samples** · Architecture · Resources |
| `panel`        | TL;DR · Top highlights · Why it matters · Resources |
| `lab`          | TL;DR · Why it matters · Session summary · **Code & samples** · Caveats · Resources |
| `lightning`    | TL;DR · Top highlights · Resources |
| `announcement` | TL;DR · **Key announcements** · Why it matters · Resources |

굵게 표시된 섹션은 해당 타입의 시그니처 — 비워 두지 말 것.

### Block-level status callouts

표 안의 inline status chip과 별개로, 본문에서 발표 1건을 강조할 때 다음 타입드 admonition을 사용:

```markdown
!!! ga "GA · 2026-06-16"
!!! preview "Public Preview"
!!! preview-private "Private Preview"
!!! limited "Limited Availability"
!!! roadmap "Roadmap"
!!! event "Event"
```

좌측 컬러 border + 마스크된 SVG 아이콘 + tinted 헤더가 자동 적용됨.

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

- 세션 노트 안의 6개 카테고리 **순서**를 임의 변경.
- 섹션 헤딩 **이름** 임의 변경 (조건에 따라 통째 삭제만 함).
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
