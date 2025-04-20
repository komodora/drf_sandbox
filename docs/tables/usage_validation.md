# usage_validation

## カラム情報

| No. | カラム名 | 日本語名 | 型 | max_length | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | BigAutoField | - | ✅ | ✅ | ❌ | - | - | - |
| 2 | length | 文字列長制限 | CharField | 20 | ❌ | ❌ | ❌ | - | - | - |
| 3 | positive_even | 正の偶数 | IntegerField | - | ❌ | ❌ | ❌ | - | - | - |
| 4 | unique | ユニーク制限 | CharField | 20 | ❌ | ✅ | ❌ | - | - | - |
| 5 | choices | 選択式 | CharField | 20 | ❌ | ❌ | ❌ | 1: a<br>2: b<br>3: c | - | - |
| 6 | ref_id | 参照先 | ForeignKey | - | ❌ | ❌ | ❌ | - | usage_validationreference | CASCADE |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
