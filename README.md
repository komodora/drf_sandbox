# drf_sandbox

## 環境

- package manager: [pdm](https://pdm-project.org/en/stable/)
- linter, formatter: [ruff](https://docs.astral.sh/ruff/)

## ディレクトリ構成

- src: DRF関係のsrc
  - sandbox: Django Project ディレクトリ
    - usage: Django Application ディレクトリ
      - \<feature>: 各機能のお試し場
  - tests: テストディレクトリ

## 実装機能

- django-debug-toolbar
- APIドキュメントの生成
  - swagger: `/api/schema/swagger-ui/`
  - redoc: `/api/schema/redoc/`
- [configの分割](src/sandbox/config/settings/base.py)
- [共通カラム](src/sandbox/usage/models/models_common_column.py)
- [独自exception_handler](src/sandbox/usage/custom_exception/views.py)
- [modelsファイルの分割](src/sandbox/usage/models/__init__.py)
- ネストされたレスポンス

追加予定
- djangoカスタムコマンド
- middleware
- カバレッジ
- bulk create
- signals
- validation