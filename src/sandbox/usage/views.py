from rest_framework import viewsets

from usage.models import User
from usage.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer
