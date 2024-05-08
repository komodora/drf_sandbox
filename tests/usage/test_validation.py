from django.test import TestCase

from src.sandbox.usage.validation.serializer import (
    CustomizingValidationSerializer,
    DefaultListSerializer,
    DefaultSerializer,
    OverrideFieldOptionSerializer,
    ValidationReferenceSerializer,
)


class ValidationTest(TestCase):
    """基本的なシリアライザを使ったバリデーションのテスト"""

    @classmethod
    def setUpTestData(cls) -> None:
        """ユニーク制限のために事前に作成"""
        data = {"name": "initial"}
        serializer = ValidationReferenceSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        data = {
            "length": "12345678901234567890",
            "positive_even": 2,
            "unique": "aaaaa",
            "choices": 1,
            "ref": "initial",
        }
        serializer = DefaultSerializer(data=data)
        serializer.is_valid()
        serializer.save()

    def test_serializer_valid(self):
        data = {
            "length": "12345678901234567890",
            "positive_even": 10,
            "unique": "bbbbb",
            "choices": 1,
            "ref": "initial",
        }
        serializer = DefaultSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)

    def test_serializer_invalid(self):
        """モデルに定義された制約は自動でバリデーションしてくれる"""

        data = {
            "length": "123456789012345678901",
            "positive_even": -3,
            "unique": "aaaaa",
            "choices": 4,
            "ref": "nonref",
        }
        serializer = DefaultSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

        # MEMO: serializer.errorsはdictのサブクラス
        # keyにはフィールド名が入ってくる
        self.assertEqual(issubclass(type(serializer.errors), dict), True)
        self.assertCountEqual(
            serializer.errors.keys(),  # type: ignore
            ["length", "positive_even", "unique", "choices", "ref"],
        )

        # MEMO: serializer.errors["field_name"]はlist型
        # 複数のバリデーションエラーが入る可能性がある
        self.assertEqual(type(serializer.errors["length"]), list)  # type: ignore
        self.assertEqual(
            serializer.errors["length"],  # type: ignore
            ["この項目が20文字より長くならないようにしてください。"],
        )
        self.assertEqual(
            serializer.errors["positive_even"],  # type: ignore
            ["-3は偶数ではありません", "-3は正の数ではありません"],
        )
        self.assertEqual(
            serializer.errors["unique"],  # type: ignore
            ["この ユニーク制限 を持った validation が既に存在します。"],
        )
        self.assertEqual(
            serializer.errors["choices"],  # type: ignore
            ['"4"は有効な選択肢ではありません。'],
        )
        self.assertEqual(
            serializer.errors["ref"],  # type: ignore
            ['主キー "nonref" は不正です - データが存在しません。'],
        )

    def test_serializer_overide_field(self):
        """
        シリアライザでフィールド定義を上書きすると,
        モデルで定義されたmax_lengthなどのバリデーションが上書きされる
        """
        data = {
            "length": "123456789012345678901234567890",
        }
        serializer = OverrideFieldOptionSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)

    def test_list_serializer_unique(self):
        """
        Listシリアライザで新規同士のユニーク制限はバリデーションされない
        あくまで, childのvalidationが回されるだけ
        """
        data = [
            {
                "length": "12345678901234567890",
                "positive_even": 10,
                "unique": "aaaaa",
                "choices": 1,
                "ref": "initial",
            },
            {
                "length": "12345678901234567890",
                "positive_even": 10,
                "unique": "bbbbb",
                "choices": 1,
                "ref": "initial",
            },
            {
                "length": "12345678901234567890",
                "positive_even": 10,
                "unique": "bbbbb",
                "choices": 1,
                "ref": "initial",
            },
        ]
        serializer = DefaultListSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)

        # MEMO: ListSerializerのerrorsはlistのサブクラス
        # childのデータそれぞれのバリデーション結果がlistの要素に入ってくる
        self.assertEqual(issubclass(type(serializer.errors), list), True)
        self.assertEqual(len(serializer.errors), 3)
        self.assertEqual(
            serializer.errors[0]["unique"],  # type: ignore
            ["この ユニーク制限 を持った validation が既に存在します。"],
        )
        self.assertEqual(serializer.errors[1], {})
        self.assertEqual(serializer.errors[2], {})


class CustomizeValidationTest(TestCase):
    """各種バリデーションメソッドを定義したシリアライザのテスト"""

    @classmethod
    def setUpTestData(cls) -> None:
        """ユニーク制限のために事前に作成"""
        data = {"name": "initial"}
        serializer = ValidationReferenceSerializer(data=data)
        serializer.is_valid()
        serializer.save()

        data = {
            "length": "12345678901234567890",
            "positive_even": 10,
            "unique": "aaaaa",
            "choices": 1,
            "ref": "initial",
        }
        serializer = DefaultSerializer(data=data)
        serializer.is_valid()
        serializer.save()

    def test_meta_field_level_validation(self):
        """Metaクラスを使ったフィールドレベルのバリデーションのテスト

        Metaクラスのextra_kwargsによるバリデーションを通過しないと,
        validate_<field_name>のバリデーションは行われない.
        これを全てのフィールドで行う.
        """
        data = {
            "length": "test",
            "positive_even": 10,
            "unique": "bbbbb",
            "choices": 4,
            "ref": "initial",
        }
        serializer = CustomizingValidationSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(
            serializer.errors.keys(),  # type: ignore
            ["length", "choices"],
        )
        self.assertEqual(
            serializer.errors["length"],  # type: ignore
            ["有効なメールアドレスを入力してください。"],
        )
        self.assertEqual(
            serializer.errors["choices"],  # type: ignore
            ['"4"は有効な選択肢ではありません。'],
        )

    def test_field_level_validation(self):
        """フィールドレベルのバリデーションのテスト

        Metaクラスのextra_kwargsによるバリデーションを通過すれば,
        validate_<field_name>のバリデーションが行われる
        """
        data = {
            "length": "test1@example.com",
            "positive_even": 10,
            "unique": "bbbbb",
            "choices": 4,
            "ref": "initial",
        }
        serializer = CustomizingValidationSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertCountEqual(
            serializer.errors.keys(),  # type: ignore
            ["length", "choices"],
        )
        self.assertEqual(
            serializer.errors["length"],  # type: ignore
            ["この項目に数字は含まないでください。"],
        )
        self.assertEqual(
            serializer.errors["choices"],  # type: ignore
            ['"4"は有効な選択肢ではありません。'],
        )

    def test_meta_object_level_validation(self):
        """Metaクラスの全体バリデーションのテスト

        フィールドレベルのバリデーションを全て通過すれば, このバリデーションが行われる
        """
        data = {
            "length": "test@example.com",
            "positive_even": 10,
            "unique": "bbbbb",
            "choices": 1,
            "ref": "initial",
        }
        serializer = CustomizingValidationSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(
            serializer.errors["non_field_errors"],  # type: ignore
            ["項目 positive_even, choices は一意な組でなければなりません。"],
        )

    def test_object_level_validation(self):
        """独自定義の全体バリデーションのテスト

        Metaクラスの全体バリデーションまで通過すれば, このバリデーションが行われる
        """
        data = {
            "length": "test@example.com",
            "positive_even": 12,
            "unique": "bbbbb",
            "choices": 1,
            "ref": "initial",
        }
        serializer = CustomizingValidationSerializer(data=data)
        self.assertEqual(serializer.is_valid(), False)
        self.assertEqual(
            serializer.errors["non_field_errors"],  # type: ignore
            ['"positive_even"には"choices"の10倍の値を入れてください。'],
        )
