from rest_framework import serializers

from usage.models import User, Role


class BadOneToOneSerializer(serializers.ModelSerializer):
    # これでOneToOneFieldで繋がったモデルにアクセスできる
    # ただし、view側でselect_relatedしないとN+1問題が起こる
    # しかし、POST、PUTはできない
    login = serializers.BooleanField(source="role.login")

    class Meta:
        model = User
        fields = ["id", "name", "login"]


class GoodOneToOneSerializer(serializers.ModelSerializer):
    # POST、PUTができるように修正したもの
    # create, updateメソッドをオーバーライドし、関連先のモデルも更新しないといけない
    # 関連先のモデルのバリデーションもここで行っているので、serializerを使って更新する必要はない
    login = serializers.BooleanField(source="role.login")

    class Meta:
        model = User
        fields = ["id", "name", "login"]

    def create(self, validated_data: dict):
        role: dict = validated_data.pop("role")
        login = role.pop("login")
        user = super().create(validated_data)
        Role.objects.create(user=user, login=login)
        return user

    def update(self, instance: User, validated_data: dict):
        role: dict = validated_data.pop("role")
        login = role.pop("login")
        user = super().update(instance, validated_data)
        # OneToOneの場合はドットでアクセスできる
        user.role.login = login
        return user
