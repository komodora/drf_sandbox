"""
modelsファイルの分割

REF: https://tokibito.hatenablog.com/entry/20120515/1337058137

1. modelsディレクトリを作成する
2. modelsディレクトリ配下に分割したmodelを置く
3. __init__.pyでモデルをimportする
"""

from usage.models.models_common_column import SubModel
from usage.models.models_nested_response import Article, Role, User
from usage.models.models_validation import Validation, ValidationReference
