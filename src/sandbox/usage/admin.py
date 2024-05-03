from django.contrib import admin

from usage.models.models_common_column import SubModel
from usage.models.models_nested_response import Article, Role, User

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Article)
admin.site.register(SubModel)
