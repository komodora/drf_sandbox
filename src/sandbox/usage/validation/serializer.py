"""Serializerによる様々なValidationを検証

テストコードで挙動を確認している
tests/usage/test_validation.py

REF: https://www.django-rest-framework.org/api-guide/serializers/#validation
REF: https://www.django-rest-framework.org/api-guide/validators/
"""

from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from usage.models.models_validation import Validation, ValidationReference


class ValidationReferenceSerializer(serializers.ModelSerializer):
    """外部キー参照先のシリアライザ"""

    class Meta:
        model = ValidationReference
        fields = "__all__"


class DefaultSerializer(serializers.ModelSerializer):
    """何もカスタマイズしないシリアライザ

    MEMO: モデルで定義された制約は自動的に引き継がれる
    データ型, 文字列長, ユニークなど
    """

    class Meta:
        model = Validation
        fields = "__all__"


class OverrideFieldOptionSerializer(serializers.ModelSerializer):
    """fieldを上書きしたシリアライザ

    モデルで定義されたlengthの制約が上書きされる
    """

    length = serializers.CharField()

    class Meta:
        model = Validation
        fields = ["length"]


class DefaultListSerializer(serializers.ListSerializer):
    child = DefaultSerializer()


class CustomizingValidationSerializer(serializers.ModelSerializer):
    """各種バリデーションメソッドを定義したシリアライザ

    独自にバリデーションを定義できるところは, 以下の4箇所がある
    - Metaクラスのextra_kwargsのvalidators
    - validate_<field_name>()メソッド
    - Metaクラスのvalidators
    - validate()メソッド

    バリデーションが実行される順番は次の通り
    1. 各フィールドのバリデーション
        a. フィールドにあらかじめ規定されたバリデーション, Metaクラスで指定されたバリデーションを行う
        b. aが通過すれば, validate_<field_name>で定義したバリデーションを行う
    2. 1を全てのフィールドで行う. フィールドがシリアライザの場合は, 再帰的にこのバリデーションが行われる
    3. 2まで全て通過していれば, Metaクラスで定義された全体バリデーションを行う
    4. 3まで全て通過していれば, validateメソッドで定義された全体バリデーションを行う
    """

    def validate_length(self, value: str):
        """Field-level validation

        validate_<field_name>のメソッド名で定義
        field単体で行えるバリデーションを定義する
        """
        if any(char.isdigit() for char in value):
            raise ValidationError("この項目に数字は含まないでください。")
        return value

    def validate(self, data):
        """Object-level validation

        複数フィールド間のバリデーションなど
        """
        positive_even: int = data.get("positive_even")
        choices: int = data.get("choices")
        if choices * 10 != positive_even:
            raise ValidationError(
                '"positive_even"には"choices"の10倍の値を入れてください。'
            )
        return data

    class Meta:
        model = Validation
        fields = "__all__"

        # Field-level validation
        extra_kwargs = {"length": {"validators": [EmailValidator()]}}

        # Object-level validation
        validators = [
            UniqueTogetherValidator(
                queryset=Validation.objects.all(), fields=["positive_even", "choices"]
            )
        ]
