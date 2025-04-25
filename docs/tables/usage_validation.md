# usage_validation

## カラム情報

| No. | カラム名 | 日本語名 | 型 | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete | 補足 |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | integer | ✅ | ✅ |  |  |  |  |  |
| 2 | length | 文字列長制限 | varchar(20) |  |  |  |  |  |  |  |
| 3 | positive_even | 正の偶数 | integer |  |  |  |  |  |  |  |
| 4 | unique | ユニーク制限 | varchar(20) |  | ✅ |  |  |  |  |  |
| 5 | choices | 選択式 | varchar(20) |  |  |  | 1: a<br>2: b<br>3: c |  |  |  |
| 6 | ref_id | 参照先 | varchar(20) |  |  |  |  | [usage_validationreference](./usage_validationreference.md) | CASCADE |  |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
