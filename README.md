# drf_sandbox

## 環境

- [Django REST Framework](https://www.django-rest-framework.org/)
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
  - swagger: http://localhost:8000/api/schema/swagger-ui/
  - redoc: http://localhost:8000/api/schema/redoc/
- [configの分割](src/sandbox/config/settings/base.py)
- [カスタム認証クラス](src/sandbox/usage/authentication/README.md)
- [共通カラム](src/sandbox/usage/models/models_common_column.py)
- [独自Exception, exception_handlerの実装](src/sandbox/usage/custom_exception/views.py)
- [modelsファイルの分割](src/sandbox/usage/models/__init__.py)
- ネストされたレスポンス
- [djangoカスタムコマンドの追加](src/sandbox/usage/management/commands/batch.py)
- [middlewareの実装](src/sandbox/usage/middleware/access_log.py)
- [serializerにおけるvalidation](src/sandbox/usage/validation/serializer.py)

追加予定
- viewsのカスタマイズ
- logging
- データマイグレを含むマイグレ
- signals
- bulk create
- カバレッジ

やりたいこと
- vscodeのテストでテストケースを個別実行