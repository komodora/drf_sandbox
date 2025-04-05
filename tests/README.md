# testの書き方

## テスト用データ

1. テスト用のFIXTURESも検索対象に追加するために, settings.pyに`FIXTURE_DIRS`を追加
2. テストクラスでfixturesを宣言. 該当のFIXTURESがロードされる


## pytest-djangoの導入

[公式doc](https://pytest-django.readthedocs.io/en/latest/#)

### 設定

pytest-djangoの設定は、pyproject.tomlに書くことができる
- `pythonpath`(optional)
  - manage.pyを見つけられるように設定
- `DJANGO_SETTINGS_MODULE`
  - configの指定
- `python_files`(optional)
  - テストファイルの命名規則

```toml
[tool.pytest.ini_options]
pythonpath = ["./src/sandbox"]
DJANGO_SETTINGS_MODULE = "config.settings.local"
python_files = ["tests.py", "test_*.py", "*_tests.py"]
```

## 実行方法

pyproject.tomlに以下を追加しておくと良い
```toml
[tool.pdm.scripts]
test = "pytest"
```

次のコマンドでテスト実行
```shell
pdm test
```