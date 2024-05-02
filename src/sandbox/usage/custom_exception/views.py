"""カスタムエラーの実装検証

REF: https://www.django-rest-framework.org/api-guide/exceptions/
"""

from rest_framework import views
from rest_framework.exceptions import NotFound

from usage.custom_exception.exception import CustomBaseException
from usage.custom_exception.handler import custom_exception_handler


class ErrorResponseView(views.APIView):
    def get(self, request, *args, **kwargs):
        """CustomExceptionをraiseするview

        settingsで定義したexception_handlerで処理される"""
        raise CustomBaseException(custom_code="E999")


class ExceptionHandlerOverridedView(views.APIView):
    def get(self, request, *args, **kwargs):
        """Exceptionのメッセージが書き換えられたview

        DRFが用意しているExceptionも, detailを書き換えることでメッセージを変えられる."""
        raise NotFound(detail="custom detail", code="custom code")

    def get_exception_handler(self):
        """view個別にexception_handlerを切り替える場合は、このメソッドをオーバーライドする."""
        return custom_exception_handler
