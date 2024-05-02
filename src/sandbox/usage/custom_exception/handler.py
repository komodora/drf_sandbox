from rest_framework.exceptions import APIException
from rest_framework.views import APIView, exception_handler

from usage.custom_exception.exception import CustomBaseException


def custom_default_exception_handler(exc: APIException, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # MEMO: 次のように書くことで, exceptionが起きたviewにアクセスできる
    view: APIView = context["view"]
    print("========== View Name ==========")
    print(view.get_view_name())
    print("===============================")

    # Now add the HTTP status code to the response.
    if response is not None:
        # MEMO: デフォルトではAPIExceptionのcodeはレスポンスに含まれないので追加する.
        response.data["code"] = exc.get_codes()

    if isinstance(exc, CustomBaseException):
        response.data["code"] = exc.custom_code

    return response


def custom_exception_handler(exc: APIException, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data["code"] = exc.get_codes()

    return response
