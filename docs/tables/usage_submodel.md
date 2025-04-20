# usage_submodel

## カラム情報

| No. | カラム名 | 日本語名 | 型 | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | integer | ✅ | ✅ | ❌ | - | - | - |
| 2 | created_at | created at | datetime | ❌ | ❌ | ❌ | - | - | - |
| 3 | updated_at | updated at | datetime | ❌ | ❌ | ❌ | - | - | - |
| 4 | title | タイトル | varchar(50) | ❌ | ❌ | ❌ | - | - | - |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
