from django.db import models


# Create your models here.
class CommonModel(models.Model):
    """共通カラムが定義されたモデル

    abstract = Trueにすることで, migration対象から外れる.
    このモデルを継承して各モデルを定義することで, ここで定義されたフィールドが継承先にも適用される.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SubModel(CommonModel):
    """共通モデルを継承したモデル"""

    title = models.CharField(verbose_name="タイトル", max_length=50)

    def __str__(self) -> str:
        return self.title
