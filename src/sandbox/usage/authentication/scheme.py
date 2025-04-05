from rest_framework import authentication, exceptions, permissions


class ExampleUser:
    def __init__(self, name: str, mail: str) -> None:
        self.name = name
        self.mail = mail
        self.is_authenticated = True


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        credentials = "hoge's_jwt"
        if not credentials:
            return None

        try:
            user = ExampleUser("hoge", "hoge@example.com")
        except Exception:
            raise exceptions.AuthenticationFailed("No such user")

        return (user, credentials)

    def authenticate_header(self, request):
        return 'Bearer realm="example"'


class ExampleAccessPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)
