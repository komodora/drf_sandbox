from rest_framework import authentication, exceptions


class ExampleAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        credentials = "hoge's_jwt"
        if not credentials:
            return None

        try:
            user = {"name": "hoge", "mail": "hoge@example.com"}
        except Exception:
            raise exceptions.AuthenticationFailed("No such user")

        return (user, credentials)

    def authenticate_header(self, request):
        return 'Bearer realm="example"'
