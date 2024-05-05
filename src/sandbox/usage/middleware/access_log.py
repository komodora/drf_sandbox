"""middlewareの定義の仕方

middlewareとは, 各request/responseで共通で処理したいことを追加定義することができるところ

REF: https://docs.djangoproject.com/en/5.0/topics/http/middleware/

1. 下の例のような, __init__, __call__メソッドを定義したクラスを実装する
2. configファイルのMIDDLWWAREのリストに追加する
    【注意】リストの順番でmiddlewareが呼び出されることに注意
"""

from datetime import datetime

from django.core.handlers.wsgi import WSGIRequest
from rest_framework.response import Response


class AccessLogMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization.
        print("INIT MIDDLEWARE")
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        # viewもしくは後続のmiddlewareの前に実行される
        method = request.method
        path = request.path
        now = datetime.now()
        print(f"START:  {now} {method} {path}")

        # viewもしくは後続のmiddlewareを呼ぶ
        response: Response = self.get_response(request)

        # viewが呼び出されたあとの処理
        now = datetime.now()
        status_code = response.status_code
        print(f"FINISH: {now} {method} {path} {status_code}")

        return response
