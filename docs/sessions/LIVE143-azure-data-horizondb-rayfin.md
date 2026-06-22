---
session_id: LIVE143
session_type: panel
title: "What's New in Azure Data: HorizonDB and Rayfin"
speakers:
  - "Nikisha Reyes-Grange (Senior Director, Azure Data and AI, Microsoft)"
  - "Charles Feddersen (Partner Director of Program Management, Postgres & MySQL on Azure, Microsoft)"
  - "Sachin Patney (General Manager, App Development for Azure Data, Microsoft)"
track: "Cloud platform & data"
level: 200
duration_min: 15
tags:
  - horizondb
  - rayfin
  - postgresql
  - fabric
  - hybrid-search
  - hnsw
  - ivfflat
  - knowledge-graph
  - ai-pipelines
  - open-source
status: draft
last_updated: 2026-06-22
---

# [LIVE143] What's New in Azure Data: HorizonDB and Rayfin

## TL;DR

> Broadcast Stage 15분 라이브 패널 (Nikisha Reyes-Grange · Charles Feddersen · Sachin Patney). 두 가지 announce를 묶어 소개:
>
> - **Azure HorizonDB** Public Preview — Satya 키노트 announce. 자세한 내용은 [DEM364](DEM364-horizondb-postgresql.md).
> - **Rayfin** — Copilot/Replit 같은 *prototyping* 환경과 *enterprise-grade production* 사이의 갭을 메우는, TypeScript 코드로 백엔드를 정의하는 open-source(MIT) SDK + CLI. 배포 시 동일 코드가 Microsoft Fabric 위의 governed 서비스로 자동 변환.
>
> 함께 Microsoft가 upstream PostgreSQL의 주요 기여자임을 강조 — 다가오는 PG 19 코드베이스의 약 8% 변경.

## Top highlights

### 1. Azure HorizonDB — Public Preview

- PostgreSQL 호환 cloud-native DBaaS, AI pipelines · hybrid search · HNSW/IVFlat 인덱스 · graph · VS Code 통합 — 본 패널에서는 헤드라인만, 데모·아키텍처·BYOM·운영 인자는 [DEM364](DEM364-horizondb-postgresql.md) 참고
- LIVE143이 추가로 명시한 사실 두 가지: **HNSW / IVFlat 인덱스 옵션** 공식 언급, **graph 관계를 VS Code 확장으로 시각화**

### 2. Rayfin — prototyping과 enterprise production 사이를 메우는 backend-as-code

> **핵심은 갭** — GitHub Copilot · Replit 같은 app-building 환경은 *rapid prototyping*에는 강하지만 enterprise-grade production deployment까지 이어지지 않음. Rayfin은 그 사이의 갭을 메우는 것을 목표로 높임. 개발자는 동일한 TypeScript 쇒로 데이터 모델을 정의하고, 그 정의가 프로토타입에서는 가벼운 로컬/SaaS 백엔드로, 프로덕션에서는 Microsoft Fabric의 governance·인증·스케일 계층이 붙은 governed 서비스로 그대로 이어짐.

- [microsoft/rayfin](https://github.com/microsoft/rayfin) — Microsoft Fabric 위의 Backend-as-a-Service (BaaS) 플랫폼, **MIT 라이선스로 GitHub 공개** (Build 시점 hub repo 셋업, 다수 `@microsoft/rayfin-*` npm 패키지 공개)
- README 정의: "**TypeScript decorators로 데이터 모델을 정의**하면 Rayfin이 백엔드(Database · Authentication · Data APIs · Storage · Hosting)를 provision · 운영"
- CLI: `npm create @microsoft/rayfin@latest` (프로젝트 scaffold) → `npx rayfin up` (배포·실행) — 이 두 명령이 prototype-to-production 경로의 entry point
- Fabric은 SaaS / zero-infra 플랫폼이므로 Rayfin으로 호스팅한 앱은 **데이터 이동 없이** Fabric 안에서 분석 · 거버넌스와 공존 ("Rayfin apps inherit enterprise-grade security and governance out of the box" — README)
- **Local Development (Experimental)** — 클라우드 리소스 없이 로컬에서 시도 가능 (`microsoft/awesome-rayfin` 의 `todo-local-experimental` 템플릿) — 이 단계가 prototyping 임

### 3. Microsoft의 upstream PostgreSQL 기여 (커뮤니티 메시지)

- 다가오는 PostgreSQL 19에서 **코드베이스의 ~8% 수정** — Microsoft가 upstream 주요 기여자 중 하나
- 클라우드 규모 PG 운영 인사이트가 upstream으로 환원, 글로벌 최대 virtual Postgres 이벤트 · 팟캐스트 · 커뮤니티 컨퍼런스 참여
- 메시지: Azure 위 PG는 "lock-in"이 아니라 "upstream 환원" — OSS 보존을 우려하는 조직 대응용 근거

## Why it matters

- **Rayfin의 시장 위치 = "vibe-coded prototype→governed production" 경로를 메우는 레이어** — 현재의 app-building 플랫폼(Copilot, Replit 등)은 초기 프로토타입을 만드는 데 뛰어나지만, 그 결과물을 인증·거버넌스·스케일이 갖춰진 production 환경으로 옮기는 구간이 항상 비용 폴이는 곳. Rayfin은 개발자가 *다시 쓰지 않고* 동일 코드/쇒를 Fabric 위의 governed 서비스로 옮기도록 설계 — 프로토타입과 프로덕션이 같은 세만틱을 공유.
- **Fabric SaaS 위에 올린다는 것의 뜻** — 외부로 데이터 movement 없이 operational + 분석 + governance를 동일 플랫폼에서 처리. 데이터 거버넌스·규제가 엄격한 조직이 prototype 이후 "무거운 ETL/IAM 재구축"을 생략하는 경로.
- **HorizonDB 진입을 라이브로 한 번에 정리** — DEM364 시청 전 컨텍스트 또는 시청 후 정리용.

## Key announcements

| 항목 | 상태 | 비고 |
|------|------|------|
| **Azure HorizonDB** | Public Preview · 2026-06 | Build event 시점 Public Preview 진입. PG 호환 + disaggregated storage + AI pipelines(async) + hybrid search + HNSW/IVFlat(+ DEM364의 DiskANN) + graph + VS Code 통합. 상세는 [DEM364](DEM364-horizondb-postgresql.md). |
| **Rayfin** | Open-source · MIT | Fabric BaaS 플랫폼. [microsoft/rayfin](https://github.com/microsoft/rayfin) (MIT), [Docs](https://aka.ms/rayfin/docs), [Templates](https://github.com/microsoft/awesome-rayfin). TypeScript decorator로 데이터 모델 정의 → DB · Auth · Data APIs · Storage · Hosting을 Fabric 위에 provision. CLI: `npm create @microsoft/rayfin@latest`, `npx rayfin up`. |

!!! event "Microsoft Build 2026 · 2026-06-03 · Broadcast Stage (Gateway Pavilion, Level 1)"
    HorizonDB Public Preview 진입과 Rayfin announce를 동시에 다룬 15분 broadcast 패널. HorizonDB는 별도 Public Preview 발표, Rayfin은 본 세션이 가장 구체적인 announce 자리 중 하나.

## Caveats & open questions

- **Rayfin은 "open-source 예정"이 아니라 이미 MIT로 공개** — LIVE143 AI summary는 발표 톤상 "will be open-sourced"라 표현했지만, [microsoft/rayfin](https://github.com/microsoft/rayfin) repo는 Build 시점에 이미 hub repo 셋업 완료 + `@microsoft/rayfin-*` npm 패키지가 공개되어 있음. 본문 표·하이라이트는 README 검증 사실로 정정.
- **HorizonDB hybrid search · HNSW · IVFlat · graph 시각화** — 본 세션에서 언급된 사실이지만, 본문은 DEM364 + [HorizonDB docs](https://learn.microsoft.com/en-us/azure/horizondb/)의 verbatim 페이지로 cross-check 권장 (HNSW/IVFlat 별도 페이지 fetch는 본 노트 작성 시점에 미수행).
- **"PG 19에서 ~8% 코드 수정"** 수치 — 발표 멘트 인용. upstream PostgreSQL commit log·릴리스 노트로 cross-check 권장.
- **Spelling cross-check** — Build 세션 페이지의 정식 표기 우선:
    - 제품/도구: `HorizonDB` (한 단어), `Rayfin` ✅  *(AI summary에 등장하는 `Horizon DB`, `Raefen`은 transcript phonetic typo)*
    - Speaker: `Charles Feddersen`, `Sachin Patney` ✅  *(AI summary의 `Federsen`, `Patne`는 typo)*
- **Rayfin과 Copilot / Replit 연동의 구체 동작** — 세션은 "deploy managed backends directly into their Fabric environments"만 짚었고 어떤 contract / IaC artifact / handoff 매커니즘인지 미공개. README에도 Copilot/Replit 통합 path는 명시 안 됨.

## Resources

- 🎥 Session: <https://build.microsoft.com/en-US/sessions/LIVE143?source=sessions>
- 📥 Video / Transcript: 세션 페이지의 "Download Video" / "Download Transcript" (Microsoft Build 로그인 필요)
- � Rayfin GitHub (MIT): <https://github.com/microsoft/rayfin>
- 📚 Rayfin Docs: <https://aka.ms/rayfin/docs> · Website: <https://aka.ms/rayfin>
- 🧰 Rayfin Templates: [microsoft/awesome-rayfin](https://github.com/microsoft/awesome-rayfin)
- 📚 HorizonDB Docs: <https://learn.microsoft.com/en-us/azure/horizondb/>
- 👤 Speakers:
    - [Charles Feddersen (LinkedIn)](https://www.linkedin.com/in/charles-feddersen-66186b25/)
    - [Sachin Patney (LinkedIn)](https://www.linkedin.com/in/spatney/) · [GitHub](https://github.com/spatney)

## Related sessions

세션 페이지가 명시한 관련 세션:

- [DEM364 — Simplify app dev with cloud-native PostgreSQL in Azure HorizonDB](DEM364-horizondb-postgresql.md) — 본 세션의 HorizonDB 부분에 대한 deep dive
- [LTG403 — MCP does way more than you think](https://build.microsoft.com/en-US/sessions/LTG403?source=sessions)
- [DEM301 — Rethinking CI: Actions, AI Agents, and the End of Commit-Fail-Commit](https://build.microsoft.com/en-US/sessions/DEM301?source=sessions)
- [ODSP916 — Design systems for every user, including people and LLMs](https://build.microsoft.com/en-US/sessions/ODSP916?source=sessions)
