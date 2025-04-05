from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .scheme import ExampleAuthentication


class ExampleAuthenticationView(APIView):
    authentication_classes = [ExampleAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {
            "user": str(request.user.name),
            "auth": str(request.auth),
        }
        return Response(content)


class JwtAuthenticationView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth),
        }
        return Response(content)
