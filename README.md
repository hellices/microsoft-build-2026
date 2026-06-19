# Microsoft Build 2026 — Session Notes

Microsoft Build 2026 주요 세션을 고객 관점에서 정리한 노트입니다.
각 세션은 동일한 템플릿으로 작성되어 빠르게 비교·검토할 수 있습니다.

- 📅 **Event**: Microsoft Build 2026
- 🎯 **Audience**: 엔터프라이즈 고객, 솔루션 아키텍트
- 📝 **Template**: [`sessions/_TEMPLATE.md`](sessions/_TEMPLATE.md)
- 👀 **Example**: [`sessions/BRK000-example-session.md`](sessions/BRK000-example-session.md) — 채워진 모습 예시

## How to read

각 세션 노트는 다음 순서로 구성됩니다.

1. **TL;DR** — 한 줄 요약
2. **Why it matters** — 고객 관점 시사점
3. **Key announcements** — GA / Preview / SDK
4. **Session summary** — 섹션별 요약
5. **Demo highlights** — 데모 타임스탬프
6. **Customer takeaways** — 도입 시 점검 항목
7. **Resources** — 원본 링크

## Sessions

### 🎤 Keynotes

| ID | Title | Status |
|----|-------|--------|
| [KEY01](sessions/KEY01-opening-keynote.md) | Microsoft Build opening keynote | 🔜 |
| [BRK226](sessions/BRK226-inside-azure-innovations.md) | Inside Azure innovations with Mark Russinovich | 🔜 |

### 🤖 Agents & Foundry

| ID | Title | Status |
|----|-------|--------|
| [BRK240](sessions/BRK240-context-aware-agents.md) | Build context-aware agents: From data to decisions | 🔜 |
| [BRK243](sessions/BRK243-claw-agent-harness.md) | Claw and agent harness in Microsoft Foundry | 🔜 |
| [BRK246](sessions/BRK246-foundry-iq.md) | Foundry IQ: Fuel agents with enterprise knowledge and agentic | 🔜 |
| [BRK251](sessions/BRK251-agent365.md) | Build secure and enterprise-ready agents with Agent 365 | 🔜 |
| [DEM330](sessions/DEM330-multimodal-agents.md) | Build multimodal agents that reason, interact, and take action | 🔜 |
| [DEMSP390](sessions/DEMSP390-multimodal-persistent-memory.md) | Create multimodal AI agents with persistent memory | 🔜 |

### 🔭 Observability & FinOps for AI

| ID | Title | Status |
|----|-------|--------|
| [BRK250](sessions/BRK250-observe-control-agents.md) | Observe and control agents across any framework with open source tools | 🔜 |
| [BRK252](sessions/BRK252-observability-to-roi.md) | From observability to ROI for AI agents on any framework | 🔜 |
| [ODSP907](sessions/ODSP907-monitor-genai-applications.md) | Monitor GenAI applications beyond golden signals | 🔜 |

### 🗄️ Data Platform

| ID | Title | Status |
|----|-------|--------|
| [DEM364](sessions/DEM364-postgres-horizondb.md) | Simplify app dev with cloud-native PostgreSQL in Azure HorizonDB | 🔜 |
| [DEM368-R1](sessions/DEM368-R1-data-science-fabric.md) | Data Science & Machine Learning with Microsoft Fabric | 🔜 |
| [LIVE143](sessions/LIVE143-azure-data-horizondb-rayfin.md) | What's New in Azure Data: HorizonDB and Rayfin | 🔜 |
| [OD823](sessions/OD823-semantic-caching-redis.md) | Faster AI Responses with Semantic Caching in Azure Managed Redis | 🔜 |

### 🔐 Security & Supply Chain

| ID | Title | Status |
|----|-------|--------|
| [ODSP938](sessions/ODSP938-software-supply-chain-github.md) | Mitigate software supply chain risks in GitHub Actions | 🔜 |
| [DEM350](sessions/DEM350-github-agentic-workflows.md) | GitHub Agentic Workflows: Automation That Actually Reads the Room | 🔜 |

### 📱 On-device & Edge

| ID | Title | Status |
|----|-------|--------|
| [BRKSP90](sessions/BRKSP90-on-device-ai-snapdragon.md) | Stop routing docstrings to 70B models with on-device AI on Snapdragon | 🔜 |

> Status: 🔜 예정 · ⏳ 작성 중 · ✅ 완료

## Themes

세션 정리가 완료된 후 주제별로 묶어 시사점을 정리합니다.

- [Agents](themes/agents.md)
- [Observability](themes/observability.md)
- [Data Platform](themes/data-platform.md)
- [Security](themes/security.md)

## Site

이 저장소는 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 기반의
GitHub Pages 사이트로도 제공됩니다.

> <https://hellices.github.io/microsoft-build-2026/>

로컬 미리보기:

```bash
pip install mkdocs-material
mkdocs serve
```

## License & attribution

본 저장소의 원본 정리물은 [CC BY 4.0](LICENSE)으로 배포됩니다.
세션 콘텐츠의 저작권은 Microsoft Corporation에 있으며, 본 저장소는 공개된 세션 자료
기반의 비공식 2차 정리물입니다. 원본은 각 노트 하단 Resources 링크를 참조하세요.
