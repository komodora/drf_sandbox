from rest_framework import status
from rest_framework.exceptions import APIException


class CustomBaseException(APIException):
    """プロジェクトで定義したExceptionクラス

    このExceptionクラスを継承して、各Exceptionを定義する
    custom_codeが開発者用のエラーコードに相当
    """

    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Custom exception is raised."
    default_code = "custom base exception"
    custom_code: str

    def __init__(self, custom_code: str, detail=None, code=None):
        self.custom_code = custom_code
        super().__init__(detail, code)
