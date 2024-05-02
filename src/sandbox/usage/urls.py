from django.urls import include, path
from rest_framework import routers

from usage.custom_exception import views as error_views
from usage.nested_response import views

router = routers.DefaultRouter()
router.register(r"one-to-one/bad", views.BadOneToOneView)
router.register(r"one-to-one/good", views.GoodOneToOneView)
router.register(r"one-to-one/easy", views.EasyOneToOneView)
router.register(r"one-to-many/easy", views.EasyOneToManyView)

urlpatterns = [
    path("", include(router.urls)),
    path("error/default", error_views.ErrorResponseView.as_view()),
    path("error/only", error_views.ExceptionHandlerOverridedView.as_view()),
]
