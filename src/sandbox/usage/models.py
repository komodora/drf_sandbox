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


class User(models.Model):
    name = models.CharField(verbose_name="氏名", max_length=20)

    def __str__(self) -> str:
        return self.name


class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login = models.BooleanField(verbose_name="ログイン権限")

    def __str__(self) -> str:
        return self.user.name


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="article")
    title = models.CharField(verbose_name="タイトル", max_length=50)

    def __str__(self) -> str:
        return self.title
