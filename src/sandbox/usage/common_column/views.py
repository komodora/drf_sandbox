from rest_framework import serializers, viewsets

from usage.models import SubModel


class SubModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubModel
        fields = ["created_at", "updated_at", "title"]


class SubModelView(viewsets.ModelViewSet):
    queryset = SubModel.objects.all()
    serializer_class = SubModelSerializer
