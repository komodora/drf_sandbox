from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from usage.authentication import views as authentication_views
from usage.common_column.views import SubModelView
from usage.custom_exception import views as error_views
from usage.nested_response import views

router = routers.DefaultRouter()
router.register(r"one-to-one/bad", views.BadOneToOneView)
router.register(r"one-to-one/good", views.GoodOneToOneView)
router.register(r"one-to-one/easy", views.EasyOneToOneView)
router.register(r"one-to-many/easy", views.EasyOneToManyView)
router.register(r"common-model", SubModelView)

urlpatterns = [
    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "authenticated/example",
        authentication_views.ExampleAuthenticationView.as_view(),
    ),
    path("authenticated/jwt", authentication_views.JwtAuthenticationView.as_view()),
    path("", include(router.urls)),
    path("error/default", error_views.ErrorResponseView.as_view()),
    path("error/only", error_views.ExceptionHandlerOverridedView.as_view()),
]
