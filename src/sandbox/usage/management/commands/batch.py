"""djangoのカスタムコマンドの作り方

1. application配下にmangement/modelsディレクトリを作り,
    __init__.pyを置く
2. <command_name>.pyを作る
3. BaseCommandクラスを継承し、handleメソッドに処理を定義する

"""

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "batchコマンド"

    def handle(self, *args, **options):
        """処理内容

        modelへのアクセスなどもできる
        """
        all_models = apps.get_models()
        for model in all_models:
            print(model)

    def add_arguments(self, parser):
        """追加の引数定義

        argparseと同じように使える
        """
        pass
