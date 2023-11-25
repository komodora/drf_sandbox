from rest_framework import viewsets

from usage.models import User
from usage.serializers import (
    BadOneToOneSerializer,
    GoodOneToOneSerializer,
    EasyOneToOneSerializer,
    EasyOneToManySerializer,
)


class BadOneToOneView(viewsets.ModelViewSet):
    # フィールド定義されていない側からでも、OneToOneFieldならselect_relatedできる
    queryset = User.objects.select_related("role")
    serializer_class = BadOneToOneSerializer


class GoodOneToOneView(viewsets.ModelViewSet):
    queryset = User.objects.select_related("role")
    serializer_class = GoodOneToOneSerializer


class EasyOneToOneView(viewsets.ModelViewSet):
    queryset = User.objects.select_related("role")
    serializer_class = EasyOneToOneSerializer


class EasyOneToManyView(viewsets.ModelViewSet):
    queryset = User.objects.prefetch_related("article")
    serializer_class = EasyOneToManySerializer
