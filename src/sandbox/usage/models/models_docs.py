from django.db import models


class DocsMain(models.Model):
    CHOICES = [(0, "alpha"), (1, "bravo"), (2, "charlie")]

    uuid = models.UUIDField(verbose_name="uuid", unique=True)
    title = models.CharField(verbose_name="タイトル", max_length=50, unique=True)
    char_field = models.CharField(verbose_name="20文字まで", max_length=20)
    text_field = models.TextField(verbose_name="テキスト")
    integer_field = models.IntegerField(verbose_name="整数", null=True)
    date_field = models.DateField(verbose_name="日付", auto_now_add=True)
    date_time_field = models.DateTimeField(verbose_name="日時", auto_now=True)
    choices = models.IntegerField(verbose_name="選択式", choices=CHOICES)

    class Meta:
        db_table = "docs_main"
        constraints = [
            models.UniqueConstraint(
                fields=["char_field", "text_field"],
                name="unique_char_field_and_text_field",
            ),
            models.CheckConstraint(
                check=models.Q(integer_field__gte=0), name="integer_field_non_negative"
            ),
        ]

    def __str__(self) -> str:
        return self.title


class DocsForeignKey(models.Model):
    name = models.TextField(verbose_name="名前")
    ref = models.ForeignKey(
        DocsMain,
        on_delete=models.CASCADE,
        verbose_name="DocsMainへの参照",
        related_name="docs_foreign_key",
    )

    class Meta:
        db_table = "docs_foreign_key"

    def __str__(self) -> str:
        return self.name


class DocsManyToMany(models.Model):
    name = models.TextField(verbose_name="名前")
    ref = models.ManyToManyField(DocsMain)

    class Meta:
        db_table = "docs_many_to_many"

    def __str__(self):
        return self.name
