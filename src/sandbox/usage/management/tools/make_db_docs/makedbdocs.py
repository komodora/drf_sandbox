import os
from typing import TypedDict

from django.apps import apps
from django.db import models
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
    field_type: str
    null: bool | None
    unique: bool | None
    primary_key: bool | None
    verbose_name: str
    is_relation: bool
    related_model: RelatedModelInfo | None
    choices: list[ChoiceInfo] | None
    on_delete: str | None
    max_length: int | None


class UniqueConstraintInfo(TypedDict):
    name: str
    fields: tuple[str]


class ModelInfo(TypedDict):
    table_name: str
    model_name: str
    fields: list[FieldInfo]
    unique_constraints: list[UniqueConstraintInfo]


class ModelsManager:
    def __init__(self) -> None:
        all_models = apps.get_models()
        app_models = [
            model
            for model in all_models
            if not model.__module__.startswith("django.contrib")
        ]

        self.models: list[ModelInfo] = []

        # モデル情報の収集
        for model in app_models:
            model_info: ModelInfo = {
                "table_name": model._meta.db_table,
                "model_name": model.__name__,
                "fields": [],
                "unique_constraints": [],
            }

            # フィールド情報の収集
            for field in model._meta.get_fields():
                field_info = ModelsManager.get_field_info(field)
                if field_info:
                    model_info["fields"].append(field_info)

            for constraint in model._meta.constraints:
                if isinstance(constraint, models.UniqueConstraint):
                    unique_constraint_info: UniqueConstraintInfo = {
                        "name": constraint.name,
                        "fields": constraint.fields,
                    }
                    model_info["unique_constraints"].append(unique_constraint_info)

            self.models.append(model_info)

    @staticmethod
    def get_field_info(field: Field | ForeignObjectRel) -> FieldInfo | None:
        # 逆参照などを除いた、DBのテーブルにカラムとして存在するフィールドであるかを判定
        if hasattr(field, "column") and field.column:  # type: ignore
            field_info: FieldInfo = {
                "column_name": field.column,  # type: ignore
                "verbose_name": str(getattr(field, "verbose_name", "")),
                "field_type": field.get_internal_type(),
                "max_length": getattr(field, "max_length", None),
                "primary_key": getattr(field, "primary_key", None),
                "unique": getattr(field, "unique", None),
                "null": getattr(field, "null", None),
                "is_relation": field.is_relation,
                "related_model": None,
                "choices": None,
                "on_delete": None,
            }

            # choices
            if getattr(field, "choices", None):
                field_info["choices"] = [
                    {"value": choice[0], "label": str(choice[1])}
                    for choice in field.choices  # type: ignore
                ]

            # relation
            if isinstance(field, ForeignKey | OneToOneField | ManyToManyField):
                related = field.related_model
                if related:
                    field_info["related_model"] = {
                        "model": related.__name__,
                        "table": related._meta.db_table,
                        "verbose_name": field.verbose_name,
                        "related_name": field.related_query_name(),
                    }

                # on_delete
                if field.remote_field.on_delete:  # type: ignore
                    field_info["on_delete"] = field.remote_field.on_delete.__name__  # type: ignore
        else:
            return None

        return field_info


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
                "| No. | カラム名 | 日本語名 | 型 | max_length | 主キー | ユニーク | NULL | 選択肢 | リレーション | on_delete |\n"
            )
            table_md.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
            for i, field in enumerate(model["fields"], start=1):
                choices = "-"
                if field["choices"]:
                    choices = "<br>".join(
                        [f"{c['value']}: {c['label']}" for c in field["choices"]]
                    )

                related = "-"
                if field["related_model"]:
                    related = field["related_model"]["table"]

                table_md.write(
                    f"| {i} "
                    f"| {field['column_name']} "
                    f"| {field['verbose_name']} "
                    f"| {field['field_type']} "
                    f"| {field.get('max_length', '-') or '-'} "
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
            table_lines.append(f"        {field['field_type']} {field['column_name']}")

            # 外部キーリレーション
            if field["related_model"]:
                target_table = field["related_model"]["table"]
                related_name = field["related_model"]["related_name"]
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
