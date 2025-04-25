# docs_many_to_many_ref

## カラム情報

| No. | カラム名 | 日本語名 | 型 | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete | 補足 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | integer | ✅ | ✅ |  |  |  |  |  |
| 2 | docsmanytomany_id | docsmanytomany | integer |  |  |  |  | [docs_many_to_many](./docs_many_to_many.md) | CASCADE |  |
| 3 | docsmain_id | docsmain | integer |  |  |  |  | [docs_main](./docs_main.md) | CASCADE |  |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
