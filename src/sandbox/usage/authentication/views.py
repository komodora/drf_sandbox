from rest_framework.response import Response
from rest_framework.views import APIView

from .scheme import ExampleAuthentication


class ExampleAuthenticationView(APIView):
    authentication_classes = [ExampleAuthentication]

    def get(self, request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth),
        }
        return Response(content)
