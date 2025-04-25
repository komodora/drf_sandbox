# usage_role

## カラム情報

| No. | カラム名 | 日本語名 | 型 | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete | 補足 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | integer | ✅ | ✅ |  |  |  |  |  |
| 2 | user_id | user | integer |  | ✅ |  |  | [usage_user](./usage_user.md) | CASCADE |  |
| 3 | login | ログイン権限 | bool |  |  |  |  |  |  |  |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
