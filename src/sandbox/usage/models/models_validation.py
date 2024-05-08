from django.core.exceptions import ValidationError
from django.db import models


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(
            f"{value}は偶数ではありません",
        )


def validate_positive(value):
    if value <= 0:
        raise ValidationError(
            f"{value}は正の数ではありません",
        )


class ValidationReference(models.Model):
    name = models.CharField(verbose_name="氏名", max_length=20, primary_key=True)

    def __str__(self) -> str:
        return self.name


class Validation(models.Model):
    CHOICES = [(1, "a"), (2, "b"), (3, "c")]

    length = models.CharField(verbose_name="文字列長制限", max_length=20)
    positive_even = models.IntegerField(
        verbose_name="正の偶数", validators=[validate_even, validate_positive]
    )
    unique = models.CharField(verbose_name="ユニーク制限", unique=True, max_length=20)
    choices = models.CharField(verbose_name="選択式", max_length=20, choices=CHOICES)
    ref = models.ForeignKey(
        ValidationReference, on_delete=models.CASCADE, verbose_name="参照先"
    )

    def __str__(self) -> str:
        return self.length
