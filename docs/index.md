# Microsoft Build 2026 — Session Notes

Microsoft Build 2026 주요 세션을 고객 관점에서 정리한 노트입니다.
각 세션은 동일한 템플릿으로 작성되어 빠르게 비교·검토할 수 있습니다.

- 📅 **Event**: Microsoft Build 2026
- 🎯 **Audience**: 엔터프라이즈 고객, 솔루션 아키텍트
- 📝 **Template**: [`sessions/_TEMPLATE.md`](sessions/_TEMPLATE.md)
- 👀 **Example**: [`sessions/BRK000-example-session.md`](sessions/BRK000-example-session.md) — 채워진 모습 예시

## How to read

각 세션 노트는 6개 카테고리(Summary / Context / Announcements / Deep dive / Assessment / References)에 묶인 섹션들로 구성됩니다. 자세한 규약은 [Contributing](contributing.md) 참조.

| # | 카테고리 | 대표 섹션 |
|---|---|---|
| 1 | **Summary** | TL;DR · Top highlights |
| 2 | **Context** | Why it matters · Customer scenarios |
| 3 | **Announcements** | Key announcements (표) |
| 4 | **Deep dive** | Session summary · Architecture · Demo · Code |
| 5 | **Assessment** | Caveats & open questions |
| 6 | **References** | Resources · Related sessions · Notes |

## Sessions

> 세션 노트는 작성되는 대로 아래 표에 추가됩니다. Status: 🔜 예정 · ⏳ 작성 중 · ✅ 완료

### 🎤 Keynote

오프닝/클로징 키노트. 한 자리에서 발표된 announcement를 다른 카테고리 세션 노트와 교차 참조합니다.

| ID | Title | Status |
|----|-------|--------|
| KEY01 | Microsoft Build opening keynote | 🔜 |

### 🧱 Azure Platform & Infrastructure

컴퓨트·네트워크·스토리지·기밀 컴퓨팅 등 Azure 기반 인프라 발표.

| ID | Title | Status |
|----|-------|--------|
| [BRK226](sessions/BRK226-inside-azure-innovations.md) | Inside Azure innovations with Mark Russinovich | ⏳ |

### 🤖 Agents & Foundry

에이전트 빌드·런타임·컨텍스트 레이어. Microsoft Foundry / Agent 365 / Microsoft IQ 계열.

| ID | Title | Status |
|----|-------|--------|
| [BRK240](sessions/BRK240-build-context-aware-agents.md) | Build context-aware agents: From data to decisions | ⏳ |
| BRK243 | Claw and agent harness in Microsoft Foundry | 🔜 |
| BRK246 | Foundry IQ: Fuel agents with enterprise knowledge and agentic | 🔜 |
| BRK251 | Build secure and enterprise-ready agents with Agent 365 | 🔜 |
| DEM330 | Build multimodal agents that reason, interact, and take action | 🔜 |
| DEMSP390 | Create multimodal AI agents with persistent memory | 🔜 |

### 🔭 Observability & FinOps for AI

에이전트·LLM 워크로드의 관찰·제어·ROI.

| ID | Title | Status |
|----|-------|--------|
| BRK250 | Observe and control agents across any framework with open source tools | 🔜 |
| BRK252 | From observability to ROI for AI agents on any framework | 🔜 |
| ODSP907 | Monitor GenAI applications beyond golden signals | 🔜 |

### 🗄️ Data Platform

OLTP·analytics·vector/hybrid search·캐시 등 데이터 플랫폼.

| ID | Title | Status |
|----|-------|--------|
| [DEM364](sessions/DEM364-horizondb-postgresql.md) | Simplify app dev with cloud-native PostgreSQL in Azure HorizonDB | ⏳ |
| DEM368-R1 | Data Science & Machine Learning with Microsoft Fabric | 🔜 |
| [LIVE143](sessions/LIVE143-azure-data-horizondb-rayfin.md) | What's New in Azure Data: HorizonDB and Rayfin | ⏳ |
| [OD823](sessions/OD823-managed-redis-semantic-caching.md) | Faster AI Responses with Semantic Caching in Azure Managed Redis | ⏳ |

### 🔧 DevOps & Supply Chain

GitHub Actions 위의 자동화·에이전트 워크플로우·공급망 보안.

| ID | Title | Status |
|----|-------|--------|
| [DEM350](sessions/DEM350-github-agentic-workflows.md) | GitHub Agentic Workflows: Automation That Actually Reads the Room | ⏳ |
| ODSP938 | Mitigate software supply chain risks in GitHub Actions | 🔜 |

### 📱 On-device & Edge

디바이스/엣지에서 동작하는 AI.

| ID | Title | Status |
|----|-------|--------|
| BRKSP90 | Stop routing docstrings to 70B models with on-device AI on Snapdragon | 🔜 |

## Themes

세션 정리가 완료된 후 주제별로 묶어 시사점을 정리합니다.
