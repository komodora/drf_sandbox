# Authentication and Permissions(認証と認可)

公式doc
- [Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [Permissions](https://www.django-rest-framework.org/api-guide/permissions/)

## 処理フロー
```
リクエスト
   ↓
ミドルウェア
   ↓
認証クラス (authentication_classes)
   ↓
認可クラス (permission_classes)
   ↓
ビュー関数
```

**重要ポイント**
- 認証されなくても、「エラーを返すかどうか」は `permission_classes` が判断する
- 認証されなかった場合、`request.user = AnonymousUser` として、ビューに届く


## 認証

### 認証クラスの適用方法

認証クラスを適用する方法は二種類ある
複数適用する場合、最初に指定したものから順に認証を試し、認証できた場合以降は実施しない

1. 全体に適用させる場合
```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

2. ビュー毎に適用させる場合
```py
class ExampleView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
```


### カスタム認証クラス

カスタム認証クラスを実装するには、`BaseAuthentication`を継承し、`.authenticate(self, request)`をオーバーライドする。

認証されていないリクエストのレスポンスとしては、401と403が考えられるが、401を返す場合は必ず`WWW-Authenticate`ヘッダーを含まなくてはいけない。
これを定めるには、`.authenticate_header(self, request)`をオーバーライドする

`.authenticate()`メソッドが返す選択肢は3つ
- 認証が成功した場合、`(user, auth)`のタプルを返す
  - ここで返した`user`, `auth`は、viewsの中で`request.user`, `request.auth`でアクセスできる
  - userはDjangoのUserモデルのインスタンスが基本だが、他でも構わない。ただし、`is_authenticated`はプロパティとして必要
- 認証を試みなかった場合、`None`を返し、他の認証方法をチェックする
- 認証に失敗した場合、`AuthenticationFailed`の例外をあげ、即時にエラーレスポンスを返す

## 認可

### 認可クラスの適用方法

認証と同様に全体に適用する方法と、ビュー毎に適用する方法がある

```py
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```
```py
from rest_framework.permissions import IsAuthenticated

class ExampleView(APIView):
    permission_classes = [IsAuthenticated]
```

### カスタム認証クラス

`BasePermission`を継承し、次の片方もしくは両方を定義する
- `.has_permission(self, request, view)`
- `.has_object_permission(self, request, view, obj)`

許可する場合は`True`を返し、許可しない場合は`False`を返す
###### 参考

RFC6750: [The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)
