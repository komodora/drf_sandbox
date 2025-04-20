# usage_article

## カラム情報

| No. | カラム名 | 日本語名 | 型 | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | integer | ✅ | ✅ | ❌ | - | - | - |
| 2 | user_id | user | integer | ❌ | ❌ | ❌ | - | usage_user | CASCADE |
| 3 | title | タイトル | varchar(50) | ❌ | ❌ | ❌ | - | - | - |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
