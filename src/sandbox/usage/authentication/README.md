# 認証

[公式ページ](https://www.django-rest-framework.org/api-guide/authentication/)

## 認証の適用

全体に適用させる場合
```py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
```

ビュー毎に適用させる場合
```py
class ExampleView(APIView):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
```

## カスタム認証クラス

カスタム認証クラスを実装するには、`BaseAuthentication`を継承し、`.authenticate(self, request)`をオーバーライドする。

認証されていないリクエストのレスポンスとしては、401と403が考えられるが、401を返す場合は必ず`WWW-Authenticate`ヘッダーを含まなくてはいけない。
これを定めるには、`.authenticate_header(self, request)`をオーバーライドする

`.authenticate()`メソッドが返す選択肢は3つ
- 認証が成功した場合、`(user, auth)`のタプルを返す
  - ここで返した`user`, `auth`は、viewsの中で`request.user`, `request.auth`でアクセスできる
- 認証を試みなかった場合、`None`を返し、他の認証方法をチェックする
- 認証に失敗した場合、`AuthenticationFailed`の例外をあげ、即時にエラーレスポンスを返す

## 参考

RFC6750: [The OAuth 2.0 Authorization Framework: Bearer Token Usage](https://datatracker.ietf.org/doc/html/rfc6750)
