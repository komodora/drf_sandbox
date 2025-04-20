# usage_article

## カラム情報

| No. | カラム名 | 日本語名 | 型 | max_length | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | id | ID | BigAutoField | - | ✅ | ✅ | ❌ | - | - | - |
| 2 | user_id | user | ForeignKey | - | ❌ | ❌ | ❌ | - | usage_user | CASCADE |
| 3 | title | タイトル | CharField | 50 | ❌ | ❌ | ❌ | - | - | - |
## 複合ユニーク制約

| No. | 制約名 | fields |
|---|---|---|
