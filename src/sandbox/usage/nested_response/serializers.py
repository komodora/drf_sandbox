from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from usage.models import User, Role, Article


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


#
# drf_writable_nestedを使用した場合
# 親側でWritableNestedModelSerializerを継承し、フィールドにネスト先のシリアライザを追加
#
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["login"]


class EasyOneToOneSerializer(WritableNestedModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = ["id", "name", "role"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        # idも含めないと、関連データ全部消してから作り直す
        fields = ["id", "title"]


class EasyOneToManySerializer(WritableNestedModelSerializer):
    # view側でprefetch_relatedしないとN+1問題が起こる
    article = ArticleSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "name", "article"]
