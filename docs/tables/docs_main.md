# docs_main

## カラム情報

| No. | カラム名 | 日本語名 | 型 | max_length | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | BigAutoField | - | ✅ | ✅ | ❌ | - | - | - |
| 2 | title | タイトル | CharField | 50 | ❌ | ✅ | ❌ | - | - | - |
| 3 | char_field | CharField(20) | CharField | 20 | ❌ | ❌ | ❌ | - | - | - |
| 4 | text_field | TextField | TextField | - | ❌ | ❌ | ❌ | - | - | - |
| 5 | integer_field | IntegerField | IntegerField | - | ❌ | ❌ | ✅ | - | - | - |
| 6 | date_field | DateField | DateField | - | ❌ | ❌ | ❌ | - | - | - |
| 7 | date_time_field | DateTimeField | DateTimeField | - | ❌ | ❌ | ❌ | - | - | - |
| 8 | choices | 選択式 | IntegerField | - | ❌ | ❌ | ❌ | 0: alpha<br>1: bravo<br>2: charlie | - | - |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
| 1 | unique_char_field_and_text_field | char_field, text_field |
