# docs_foreign_key

## カラム情報

| No. | カラム名 | 日本語名 | 型 | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | integer | ✅ | ✅ | ❌ | - | - | - |
| 2 | name | 名前 | text | ❌ | ❌ | ❌ | - | - | - |
| 3 | ref_id | DocsMainへの参照 | integer | ❌ | ❌ | ❌ | - | docs_main | CASCADE |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
