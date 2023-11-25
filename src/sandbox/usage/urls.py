from django.urls import include, path
from rest_framework import routers

from usage import views

router = routers.DefaultRouter()
router.register(r"one-to-one/bad", views.BadOneToOneView)
router.register(r"one-to-one/good", views.GoodOneToOneView)
router.register(r"one-to-one/easy", views.EasyOneToOneView)
router.register(r"one-to-many/easy", views.EasyOneToManyView)

urlpatterns = [
    path("", include(router.urls)),
]
