from rest_framework import serializers

from usage.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name"]
