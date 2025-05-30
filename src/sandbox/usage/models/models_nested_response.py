from django.db import models

# Create your models here.


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
