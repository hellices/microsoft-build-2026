---
session_id: ODSP938
session_type: breakout
title: "Mitigate software supply chain risks in GitHub Actions"
speakers:
  - Erika Heidi (Staff Developer Relations Engineer, Chainguard)
track: DevOps & Supply Chain
level: 200
duration_min: 15
tags: [github-actions, supply-chain, security, devsecops, chainguard, sigstore, oidc, sponsor]
status: draft
last_updated: 2026-06-23
---

# [ODSP938] Mitigate software supply chain risks in GitHub Actions

## TL;DR

> 15분짜리 Chainguard 스폰서 세션. Trivy 공격 같은 실제 사례를 베이스로 GitHub Actions 워크플로우를 굳히는 **5가지 행동 항목** 을 압축. 가이드 자체는 vendor-neutral 이라 GitHub Docs 공식 hardening 가이드와 그대로 정합.
>
> - **검사·잠금** — repo를 Copilot에 *"evaluate GitHub Actions for vulnerabilities"* 시키고, `pull_request_target` + head 코드 실행 / broad PAT / 태그 핀 / unprotected main·tags 같은 기본 함정을 잡아냄.
> - **공격 표면 축소** — 런타임에 안 쓰는 의존성 제거. 최소 컨테이너 이미지 (예: Chainguard Python 이미지 — 발표자 주장 기준 CVE 4건 vs. Docker Hub Python 579건).
> - **신뢰된 출처 + digest pin + short-lived token** — 멀웨어 98% 가 빌드/배포 단계에 주입됨. tag 대신 digest 로 pin (Digestabot으로 자동 PR), long-lived PAT 대신 Octo-STS 같은 short-lived 토큰 사용.

## Why it matters

GitHub Actions 워크플로우는 **CI/CD 신뢰 사슬의 가장 약한 고리** 가 되기 쉬움. 2025년 Trivy (aquasecurity/trivy-action) 사건이 대표적 — 공격자가 광범위 권한 PAT를 탈취해 release tag를 악성 커밋으로 재작성, 다운스트림 수십만 repo가 자동으로 감염된 코드를 끌어왔음. 본 세션은 이 사건이 가능했던 *각각의 디폴트 설정* 을 5가지 행동 항목으로 분해하고 즉시 적용 가능한 체크리스트를 제공.

세션은 Chainguard 스폰서지만 핵심 가이드(`pull_request_target` 위험 / branch protection / digest pin / short-lived token)는 모두 GitHub 공식 hardening 문서와 동일한 권고. Chainguard 제품 (minimal containers · libraries · Digestabot · Octo-STS) 은 그 권고를 *어떻게 실행하는지* 의 한 가지 옵션으로 제시됨.

## Customer scenarios

- **Platform / DevSecOps 팀** — 조직 전체 Actions workflow를 한 번에 audit해야 할 때, Copilot agent에 `"Evaluate my GitHub Actions workflows for supply chain vulnerabilities"` 식 프롬프트로 1차 스캔 후 발견된 항목을 PR 로 잡아냄.
- **OSS maintainer** — public repo + secret 사용. `pull_request_target` 으로 외부 PR이 main 컨텍스트에서 코드를 실행하면 즉시 secret 누출 위험. main 브랜치·릴리즈 태그 보호 + PR 권한 최소화 + OIDC 도입.
- **Enterprise CI/CD** — 외부 actions/containers/libraries 를 SHA digest 로 pin 하고 Renovate/Dependabot 또는 Digestabot 으로 업데이트 PR만 자동 발행 (사람 리뷰 유지).
- **Incident response** — 한 번 PAT 가 유출되면 long-lived 면 사실상 전체 org 통제권을 잃음. short-lived 토큰(OIDC + cloud federation, Octo-STS 등)으로 폭발 반경(blast radius) 을 분 단위로 제한.

## Session summary

### 1. Inspect repos for insecure defaults

발표자가 의도적으로 취약하게 세팅한 데모 repo로 secret exfiltration 시연. 가장 흔한 5개 함정:

| 함정 | 왜 위험한가 |
|---|---|
| `pull_request_target` + head 코드 실행 | 외부 PR 코드가 *main 브랜치의 secret/env 컨텍스트* 에서 실행 → secret 즉시 유출 가능. **Trivy 초기 공격에서 사용된 방법.** |
| Long-lived PAT, broad scope | 한 번 탈취되면 org 전체 권한. write 권한이면 release/tag 조작까지. |
| Direct shell execution with untrusted input | `${{ github.event.* }}` 등 외부 입력이 shell에 그대로 들어감 → 명령 주입. |
| Actions pinned by tag (`@v1`, `@v2`) | tag는 재작성 가능 — 공격자가 같은 태그를 악성 커밋으로 옮길 수 있음. **Trivy 후속 단계.** |
| Unprotected main branch + unprotected release tags | 탈취된 PAT 로 main에 직접 push / tag 재작성 가능. **기본값으로 보호 안 됨 — 설정에서 직접 켜야 함.** |

**도구 팁** — GitHub Copilot에 *"Evaluate my GitHub Actions workflows for vulnerabilities"* 라고 던지면 위 항목들을 효과적으로 찾아냄. 단발성 일괄 점검에 유용.

### 2. Minimize attack surface

원리는 단순 — *런타임에 안 쓰는 모든 것을 빼라*. 직접 의존성 뿐 아니라 **전이 의존성(transitive)** 까지 약한 고리가 됨. 발표자가 보여준 가장 실용적인 한 가지: **베이스 컨테이너 이미지를 최소 이미지로 교체**.

발표자 인용 수치(Chainguard 발표 자료 기준):

| 이미지 | 발표 시점 CVE 수 |
|---|---|
| Chainguard Python | **4** |
| Docker Hub `python:latest` | **579** |

> ⚠️ 위 수치는 Chainguard 제품 마케팅 자료 기준. 시점·버전·스캐너에 따라 변동. 비교 자체보다 *"기본 베이스 이미지에는 런타임에 필요 없는 패키지가 한가득 포함되어 있다"* 라는 방향성으로 인용.

### 3. Pull from trusted sources

발표자 주장: *"~98% 의 멀웨어는 빌드·배포 단계에 주입됨 (소스 코드 리뷰를 우회)"*. 패턴 명칭은 **ghost release** — 소스는 깨끗한데 배포된 아티팩트가 다름.

**왜 public registry 가 약한가** — npm · PyPI · Maven Central 등은 *공유·배포 편의* 가 설계 목표였고, 아티팩트 무결성 검증·tampering 방어는 상대적으로 늦게 들어옴. 공격자가 CI/CD 파이프라인이나 개발자 머신을 노드 삼아 자격증명 수집 → 같은 패키지를 빌드 시점에 변조 → 모두에게 배포되는 구조.

발표자가 제안한 한 가지 옵션: **Chainguard Libraries** (Python · Java · JavaScript) — 검증된 빌드 환경에서 만들고 pre/post-install 스크립트를 실행하지 않음. *vendor-specific 옵션이지만 카테고리(검증된 빌더 + 변조방지 배포) 자체는 [SLSA framework](https://slsa.dev/) 가 표준화 중인 영역.*

### 4. Pin by digest, not by tag

**Tag는 mutable** — 공격자가 같은 `v1` 태그를 악성 커밋으로 옮길 수 있음. Trivy 사건의 핵심 메커니즘 중 하나. **Digest는 immutable cryptographic hash** — 한 번 pin 하면 같은 빌드만 끌어옴.

예시:

```yaml
# 위험 — tag pin
- uses: actions/checkout@v4

# 권장 — 40-char SHA digest pin
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11   # v4.1.1
```

문제는 digest가 시간이 지나면 **stale** 해진다는 것. 발표자가 제안하는 자동화: **Digestabot** (Chainguard 오픈소스, 무료) — 새 버전이 나오면 digest 업데이트 PR을 자동 발행. 동일 카테고리의 다른 OSS 옵션: GitHub 네이티브 [**Dependabot**](https://docs.github.com/code-security/dependabot) (SHA pin 정책과 결합), [**ratchet**](https://github.com/sethvargo/ratchet) (다수 CI 시스템 지원), [**Renovate**](https://github.com/renovatebot/renovate) (`pinDigests: true`), [**frizbee**](https://github.com/stacklok/frizbee). 구체적 수준·운영 부담이 다르니 조직의 CI 스택에 맞게 선택.

### 5. Ban long-lived PATs

Trivy 사건의 마무리 단서 — **org-wide 권한의 long-lived PAT 가 유출되어 공격자가 전체 org 통제권 확보**. 발표자 권고:

| 안티패턴 | 권장 |
|---|---|
| Personal Access Token, expiry 1년+, broad scope | **Short-lived token** (분 단위 만료) |
| Repo secret에 토큰 평문 저장 | OIDC federation으로 cloud (Azure/AWS/GCP) 자격증명을 **워크플로우 실행 시점에만** 받기 |
| GitHub App PAT 직접 사용 | GitHub App + on-demand 단기 토큰 발급 |

발표자가 소개한 한 가지 도구: **Octo-STS** (Chainguard, 무료 GitHub app) — Sigstore/Cosign 의 키리스 서명 개념을 토큰 발급에 적용해 단기 자격증명 발행. *동등한 GitHub 네이티브 옵션*: [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) — Azure / AWS / GCP / HashiCorp Vault 와 federated identity 연결, PAT 없이도 클라우드 인증 가능.

## Code & samples

세션은 코드를 거의 노출하지 않지만 가이드를 적용할 때 참고할 만한 최소 패턴 정리:

**1. `pull_request_target` 안전 사용 (외부 PR 컨텐츠를 *체크아웃·실행하지 않을 때*)**

```yaml
on:
  pull_request_target:        # main 컨텍스트 권한 — secret 접근 가능
    types: [opened, synchronize]

permissions:
  pull-requests: write        # 최소 권한만
  contents: read

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
      # 외부 PR의 코드는 절대 실행하지 않음 — labeling/comment 등 메타 작업만
      - uses: actions/labeler@e54e5b338fbd6e6cdb5c20b0a2c5b9eaab1ba7ec   # SHA pin
```

**2. Tag → SHA digest pin 일괄 적용**

```yaml
# Before
- uses: actions/checkout@v4
- uses: docker/setup-buildx-action@v3

# After (Dependabot 또는 Digestabot 가 자동으로 주석 + SHA 갱신 PR)
- uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11   # v4.1.1
- uses: docker/setup-buildx-action@d70bba72b1f3fd22344832f00baa16ece964efeb   # v3.3.0
```

**3. PAT 대신 OIDC for Azure (PAT 한 줄도 없이 ARM에 인증)**

```yaml
permissions:
  id-token: write   # OIDC token 발급용
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: azure/login@a65d910e8af852a8061c627c456678983e180302   # v2.2.0
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}        # OIDC federated app
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}
          # client-secret 없음 — federated credential 로 OIDC 토큰 교환
```

## Caveats & open questions

- **스폰서 (Chainguard) on-demand 세션** — Microsoft 자체 발표가 아님. 다섯 가지 권고 자체는 vendor-neutral 이고 GitHub 공식 [Security hardening for GitHub Actions](https://docs.github.com/actions/security-guides/security-hardening-for-github-actions) 와 동일한 카테고리지만, 마지막 단계에서 제시된 도구 (Chainguard Libraries · Digestabot · Octo-STS) 는 Chainguard 자체 제품. 동등한 GitHub/Microsoft 네이티브 대안 존재 (Dependabot SHA pinning · GitHub Actions OIDC · GitHub App short-lived tokens).
- **"Chainguard Python 4 CVE vs Docker Hub Python 579 CVE"** — 발표자 인용. 정확한 측정 시점·이미지 태그·스캐너 미공개. 시점에 따라 변동하니 *방향성* (최소 이미지가 패키지 수·CVE 수에서 큰 차이를 만든다) 만 인용 권장.
- **"~98% 멀웨어가 빌드/배포 단계 주입"** — 발표자 인용. 정확한 원자료 미공개. 유사 통계가 [Sonatype State of the Software Supply Chain](https://www.sonatype.com/state-of-the-software-supply-chain) · ENISA 보고서에 나오지만 수치는 보고서마다 다름.
- **Trivy 공격의 정확한 timeline / IoC** — 세션에서 요약만 언급. 자세한 분석은 [GitHub Security Lab · Aqua Security 사후 보고](https://github.com/aquasecurity/trivy-action/security/advisories) 등 외부 자료 cross-check.
- **Octo-STS / Digestabot 운영 신뢰도** — Chainguard 가 호스팅하는 free GitHub app 으로, 자체 호스팅이 필요한 환경(엔터프라이즈·규제 산업)에서는 GitHub 네이티브 OIDC + cloud federation 조합이 더 적절할 수 있음.

## Resources

- 🎥 Session: <https://build.microsoft.com/en-US/sessions/ODSP938?source=sessions>
- 📥 Video / Transcript: 세션 페이지의 "Download Video" / "Download Transcript" (Microsoft Build 로그인 필요)
- 👤 Speaker: [Erika Heidi (LinkedIn)](https://www.linkedin.com/in/erikaheidi/) · [GitHub (@erikaheidi)](https://www.github.com/erikaheidi)
- 📚 **GitHub 공식 hardening docs** (본 세션 가이드의 1:1 매칭):
    - [Security hardening for GitHub Actions](https://docs.github.com/actions/security-guides/security-hardening-for-github-actions) — `pull_request_target` 위험 / SHA pin / secret 취급 가이드
    - [Security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect) — PAT 없이 cloud 인증
    - [About branch protection rules](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
    - [About tag protection rules](https://docs.github.com/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/configuring-tag-protection-rules)
    - [Keeping your actions up to date with Dependabot](https://docs.github.com/code-security/dependabot/working-with-dependabot/keeping-your-actions-up-to-date-with-dependabot)
- 📚 **GitHub blog** — [Four tips to keep your GitHub Actions workflows secure](https://github.blog/security/supply-chain-security/four-tips-to-keep-your-github-actions-workflows-secure/)
- 📚 **표준 / 프레임워크**:
    - [SLSA framework (supply chain levels)](https://slsa.dev/)
    - [Sigstore / Cosign](https://www.sigstore.dev/) — Octo-STS 가 기반한 키리스 서명 표준
    - [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
- 🔧 **세션 언급 도구** *(Chainguard, vendor-specific)*:
    - [Digestabot](https://github.com/chainguard-dev/digestabot) — digest 자동 업데이트 봇
    - [Octo-STS](https://github.com/octo-sts/app) — short-lived GitHub token issuer (Sigstore 기반)
    - [Chainguard Containers · Libraries](https://www.chainguard.dev/) — minimal images / verified library builds

## Related sessions

Build 세션 페이지가 명시한 관련 세션:

- [TT659-R1 — Outcome-maxxing, not token-maxxing: what "good" looks like in AI-authored code](https://build.microsoft.com/en-US/sessions/TT659-R1?source=sessions)
- [OD820 — Designing Reliable Multi-Agent Apps with Azure Cosmos DB](https://build.microsoft.com/en-US/sessions/OD820?source=sessions)
- [BRK222 — The honest practitioner's take on agentic AI on Kubernetes](https://build.microsoft.com/en-US/sessions/BRK222?source=sessions)

본 저장소의 인접 노트:

- [DEM350 — GitHub Agentic Workflows](DEM350-github-agentic-workflows.md) — 같은 GitHub Actions 위에서 *에이전트* 를 안전하게 실행하는 패턴 (gh-aw 의 `permissions: read-only` 기본값과 본 세션의 최소 권한 원칙이 일치).
