# Microsoft Build 2026 — Session Notes

Microsoft Build 2026의 주요 세션을 고객·아키텍트 관점에서 정리한 노트입니다.

📖 **사이트**: <https://hellices.github.io/microsoft-build-2026/>

## Repo layout

```
docs/
├── index.md                 # 사이트 홈 (세션 인덱스)
├── contributing.md          # 작성 규약
├── sessions/
│   ├── _TEMPLATE.md         # 세션 템플릿 (수정 금지, 복사해서 사용)
│   └── <ID>-<slug>.md       # 세션 1개 = 파일 1개
└── themes/
    ├── _TEMPLATE.md
    └── <topic>.md           # 주제별 큐레이션
```

- 콘텐츠는 모두 `docs/` 안에 위치 (MkDocs 빌드 대상).
- 작성 규약은 [`docs/contributing.md`](docs/contributing.md) 참조.
- 푸시하면 `.github/workflows/deploy-site.yml` 이 GitHub Pages 로 자동 배포.

## Local preview

```bash
pip install mkdocs-material
mkdocs serve   # http://127.0.0.1:8000
```

## License

본 저장소의 원본 정리물은 [CC BY 4.0](LICENSE) 으로 배포됩니다.
세션 콘텐츠의 저작권은 Microsoft Corporation 에 있으며, 본 저장소는 공개된 세션
자료 기반의 비공식 2차 정리물입니다. 원본 링크는 각 세션 노트 하단의 Resources 섹션 참조.
