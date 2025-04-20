# docs_main

## カラム情報

| No. | カラム名 | 日本語名 | 型 | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |
|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | integer | ✅ | ✅ | ❌ | - | - | - |
| 2 | uuid | uuid | char(32) | ❌ | ✅ | ❌ | - | - | - |
| 3 | title | タイトル | varchar(50) | ❌ | ✅ | ❌ | - | - | - |
| 4 | char_field | 20文字まで | varchar(20) | ❌ | ❌ | ❌ | - | - | - |
| 5 | text_field | テキスト | text | ❌ | ❌ | ❌ | - | - | - |
| 6 | integer_field | 整数 | integer | ❌ | ❌ | ✅ | - | - | - |
| 7 | date_field | 日付 | date | ❌ | ❌ | ❌ | - | - | - |
| 8 | date_time_field | 日時 | datetime | ❌ | ❌ | ❌ | - | - | - |
| 9 | choices | 選択式 | integer | ❌ | ❌ | ❌ | 0: alpha<br>1: bravo<br>2: charlie | - | - |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
| 1 | unique_char_field_and_text_field | char_field, text_field |
