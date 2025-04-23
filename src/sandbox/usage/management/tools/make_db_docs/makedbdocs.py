import os
from typing import TypedDict

from django.apps import apps
from django.db import connection, models
from django.db.models import Field
from django.db.models.fields.related import (
    ForeignKey,
    ForeignObjectRel,
    ManyToManyField,
    OneToOneField,
)


class RelatedModelInfo(TypedDict):
    model: str
    table: str
    verbose_name: str
    related_name: str


class ChoiceInfo(TypedDict):
    value: str | int
    label: str


class FieldInfo(TypedDict):
    column_name: str
    # Djangoの型
    field_type: str
    # DBの型
    db_type: str | None
    null: bool | None
    unique: bool | None
    primary_key: bool | None
    verbose_name: str
    related_model: RelatedModelInfo | None
    choices: list[ChoiceInfo] | None
    on_delete: str | None
    max_length: int | None


class UniqueConstraintInfo(TypedDict):
    name: str
    fields: tuple[str]


class CheckConstraintInfo(TypedDict):
    name: str
    check: str


class ModelInfo(TypedDict):
    table_name: str
    model_name: str
    fields: list[FieldInfo]
    unique_constraints: list[UniqueConstraintInfo]
    check_constraints: list[CheckConstraintInfo]


class ModelsManager:
    def __init__(self) -> None:
        self.models: list[ModelInfo] = []
        app_models = self.collect_models()

        for model in app_models:
            model_info = self.build_model_info(model)
            self.models.append(model_info)
            self.collect_through_models(model)

    def collect_models(self) -> list[type[models.Model]]:
        return [
            model
            for model in apps.get_models()
            if not model.__module__.startswith("django.contrib")
        ]

    def build_model_info(self, model: type[models.Model]) -> ModelInfo:
        model_info: ModelInfo = {
            "table_name": model._meta.db_table,
            "model_name": model.__name__,
            "fields": [],
            "unique_constraints": [],
            "check_constraints": [],
        }

        for field in model._meta.get_fields():
            field_info = self.get_field_info(field)
            if field_info:
                model_info["fields"].append(field_info)

        for constraint in model._meta.constraints:
            if isinstance(constraint, models.UniqueConstraint):
                model_info["unique_constraints"].append(
                    {
                        "name": constraint.name,
                        "fields": constraint.fields,
                    }
                )
            elif isinstance(constraint, models.CheckConstraint):
                model_info["check_constraints"].append(
                    {
                        "name": constraint.name,
                        "check": str(constraint.check),
                    }
                )

        return model_info

    def collect_through_models(self, model: type[models.Model]) -> None:
        for field in model._meta.get_fields():
            if isinstance(field, ManyToManyField):
                through_model = field.remote_field.through  # type: ignore
                if through_model._meta.auto_created:
                    if not any(
                        m["table_name"] == through_model._meta.db_table
                        for m in self.models
                    ):
                        through_info = self.build_model_info(through_model)
                        self.models.append(through_info)

    @staticmethod
    def get_field_info(field: Field | ForeignObjectRel) -> FieldInfo | None:
        # ManyToManyField は中間テーブル経由で定義されるので、ここではスキップ
        if isinstance(field, ManyToManyField):
            return None

        # 逆参照などを除いた、DBのテーブルにカラムとして存在するフィールドであるかを判定
        if hasattr(field, "column") and field.column:  # type: ignore
            db_type = (
                field.target_field.db_type(connection=connection)
                if isinstance(field, (ForeignKey | OneToOneField))
                else field.db_type(connection=connection)
            )

            field_info: FieldInfo = {
                "column_name": field.column,  # type: ignore
                "verbose_name": str(getattr(field, "verbose_name", "")),
                "field_type": field.get_internal_type(),
                "db_type": db_type,
                "max_length": getattr(field, "max_length", None),
                "primary_key": getattr(field, "primary_key", None),
                "unique": getattr(field, "unique", None),
                "null": getattr(field, "null", None),
                "related_model": None,
                "choices": None,
                "on_delete": None,
            }

            if getattr(field, "choices", None):
                field_info["choices"] = [
                    {"value": choice[0], "label": str(choice[1])}
                    for choice in field.choices  # type: ignore
                ]

            if isinstance(field, (ForeignKey | OneToOneField)):
                related = field.related_model
                if related:
                    field_info["related_model"] = {
                        "model": related.__name__,
                        "table": related._meta.db_table,
                        "verbose_name": field.verbose_name,
                        "related_name": field.related_query_name(),
                    }

                if field.remote_field.on_delete:  # type: ignore
                    field_info["on_delete"] = field.remote_field.on_delete.__name__  # type: ignore

            return field_info

        return None


def generate_table_definitions(models: list[ModelInfo], output_dir: str):
    """

    出力先:
        - <output_dir>
            |- tables.md
            |- tables
                |- <table_name>.md
    """
    os.makedirs(output_dir, exist_ok=True)
    output_tables_dir = f"{output_dir}/tables"
    os.makedirs(output_tables_dir, exist_ok=True)

    # 一覧用マークダウン生成
    index_md_filename = f"{output_dir}/tables.md"
    with open(index_md_filename, "w") as index_md:
        index_md.write("# テーブル一覧\n\n")

        index_md.write("| No. | モデル名 | テーブル名 | 定義ファイル |\n")
        index_md.write("|---|---|---|---|\n")
        for i, model_info in enumerate(models, start=1):
            model_md_filename = f"./tables/{model_info['table_name']}.md"
            index_md.write(
                f"| {i} "
                f"| {model_info['model_name']} "
                f"| {model_info['table_name']} "
                f"| [{model_info['table_name']}]({model_md_filename}) "
                f"|\n"
            )

    # 各テーブル定義書の生成
    for model in models:
        table_name = model["table_name"]
        filename = os.path.join(output_tables_dir, f"{table_name}.md")

        with open(filename, "w", encoding="utf-8") as table_md:
            table_md.write(f"# {table_name}\n\n")

            # カラム情報
            table_md.write("## カラム情報\n\n")
            table_md.write(
                "| No. | カラム名 | 日本語名 | 型 | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |\n"
            )
            table_md.write("|---|---|---|---|---|---|---|---|---|---|\n")
            for i, field in enumerate(model["fields"], start=1):
                choices = "-"
                if field["choices"]:
                    choices = "<br>".join(
                        [f"{c['value']}: {c['label']}" for c in field["choices"]]
                    )

                related = "-"
                if field["related_model"]:
                    related = f"[{field['related_model']['table']}](./{field['related_model']['table']}.md)"

                table_md.write(
                    f"| {i} "
                    f"| {field['column_name']} "
                    f"| {field['verbose_name']} "
                    f"| {field['db_type']} "
                    f"| {'✅' if field['primary_key'] else '❌'} "
                    f"| {'✅' if field['unique'] else '❌'} "
                    f"| {'✅' if field['null'] else '❌'} "
                    f"| {choices} "
                    f"| {related} "
                    f"| {field['on_delete'] or '-'} "
                    f"|\n"
                )

            # 複合ユニーク制約
            table_md.write("## 複合ユニーク制約\n\n")
            table_md.write("| No. | 制約名 | fields |\n")
            table_md.write("|---|---|---|\n")
            for i, unique_constraint in enumerate(model["unique_constraints"], start=1):
                table_md.write(
                    f"| {i} "
                    f"| {unique_constraint['name']} "
                    f"| {', '.join(unique_constraint['fields'])} "
                    f"|\n"
                )


def generate_er(models: list[ModelInfo], output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    relations = []
    tables = []

    for model in models:
        table_name = model["table_name"]
        fields = model["fields"]
        table_lines = [f"    {table_name} {{"]

        for field in fields:
            table_lines.append(f"        {field['db_type']} {field['column_name']}")

            # 外部キーリレーション
            if field["related_model"]:
                target_table = field["related_model"]["table"]
                related_name = field["related_model"]["related_name"].rstrip("+")
                rel = f"    {table_name} ||--|{{ {target_table} : {related_name}"
                if rel not in relations:
                    relations.append(rel)

        table_lines.append("    }")
        tables.extend(table_lines)

    with open(f"{output_dir}/er.md", "w", encoding="utf-8") as f:
        f.writelines(
            "\n".join(["```mermaid", "erDiagram"] + relations + tables + ["```"])
        )


def generate_docs():
    output_dir = "./docs"
    models_maneager = ModelsManager()
    generate_table_definitions(models_maneager.models, output_dir)
    generate_er(models_maneager.models, output_dir)
