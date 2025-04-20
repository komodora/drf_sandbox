# docs_foreign_key

## カラム情報

| No. | カラム名 | 日本語名 | 型 | max_length | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | BigAutoField | - | ✅ | ✅ | ❌ | - | - | - |
| 2 | name | name | TextField | - | ❌ | ❌ | ❌ | - | - | - |
| 3 | ref_id | DocsMainへの参照 | ForeignKey | - | ❌ | ❌ | ❌ | - | docs_main | CASCADE |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
