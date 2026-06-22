# Contributing

본 저장소의 일관성을 유지하기 위한 최소 규약입니다.

## File naming

- 세션: `sessions/<SESSION_ID>-<kebab-slug>.md`
    - 예: `sessions/BRK250-observe-control-agents.md`
    - 슬러그는 소문자·하이픈만. 관사(a/the)는 생략 가능.
- 주제: `themes/<topic>.md`

## Writing rules

- 본문은 한국어, 제품·기능명 등 고유명사는 영어 원문 유지.
- `_TEMPLATE.md`의 헤더 순서·이름은 변경하지 않음. 내용이 없으면 빈 채로 둠.
- GA / Preview 등 상태 표기 시 **확인 일자**를 함께 적음.
- 인용·참고 자료는 추측 없이 실재하는 링크만 적음.

## Frontmatter (sessions/*.md)

- 필수 필드: `session_id`, `title`, `status`, `last_updated`
- 그 외 필드는 알 수 없으면 비워둠 (필드 자체를 삭제하지는 않음).
- `status` 값: `draft` · `review` · `done`

## Status convention

| Frontmatter | README 표시 | 의미 |
|-------------|------------|------|
| `draft`     | ⏳ | 작성 중 |
| `review`    | ⏳ | 검토 요청 |
| `done`      | ✅ | 공유 가능 |
| (미작성)    | 🔜 | 예정 |

`README.md`의 표 상태와 frontmatter `status`는 일치시킵니다.

## Status callouts (block-level)

표 안의 상태 칩과 별개로, 본문에서 한 가지 발표를 강조하고 싶을 때 다음 admonition 타입을 사용할 수 있습니다.

```markdown
!!! ga "GA · 2026-06-16"
    Work IQ — M365 in-place, Chat/Context/Tools/Workspaces API

!!! preview "Public Preview"
    Manifold Direct Virtualization — VM 추론 25× 가속

!!! preview-private "Private Preview"
    Project Mosaic — workload-aware HBM/DRAM 메모리 풀

!!! limited "Limited Availability"
    NDv6 GB300 (Blackwell Ultra) 클러스터

!!! roadmap "Roadmap"
    Azure Integrated HSM — confidential AI 시그너처 보호

!!! event "Event"
    Microsoft Build 2026 · 2026-06-15 ~ 18
```

실제 렌더링:

!!! ga "GA · 2026-06-16"
    Work IQ — M365 in-place, Chat/Context/Tools/Workspaces API

!!! preview "Public Preview"
    Manifold Direct Virtualization — VM 추론 25× 가속

!!! preview-private "Private Preview"
    Project Mosaic — workload-aware HBM/DRAM 메모리 풀

!!! limited "Limited Availability"
    NDv6 GB300 (Blackwell Ultra) 클러스터

!!! roadmap "Roadmap"
    Azure Integrated HSM — confidential AI 시그너처 보호

!!! event "Event"
    Microsoft Build 2026 · 2026-06-15 ~ 18

## Adding a new session

1. `sessions/_TEMPLATE.md` 를 복사.
2. 파일명을 `<ID>-<slug>.md` 로 변경.
3. frontmatter 채우고 본문 작성.
4. `README.md` 표에 항목 추가.
5. `mkdocs.yml` 의 `nav` 에 라인 추가.

## Local preview

```bash
pip install mkdocs-material
mkdocs serve
# http://127.0.0.1:8000
```

푸시하면 `.github/workflows/deploy-site.yml` 이 GitHub Pages 로 자동 배포합니다.
