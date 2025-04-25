from django.core.management.base import BaseCommand

from ..tools.make_db_docs import makedbdocs


class Command(BaseCommand):
    help = "各種ドキュメント作成コマンド"

    def handle(self, *args, **options):
        makedbdocs.generate_docs()
