from django.contrib import admin

from usage import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Role)
admin.site.register(models.Article)
admin.site.register(models.SubModel)
