from behave import then
from django.conf import settings


@then('Django REST Framework accepts JWT bearer authentication')
def check_jwt_authentication(context):
    authentication = settings.REST_FRAMEWORK.get('DEFAULT_AUTHENTICATION_CLASSES', [])
    assert 'rest_framework_simplejwt.authentication.JWTAuthentication' in authentication


@then('CORS middleware is enabled')
def check_cors_middleware(context):
    assert 'corsheaders.middleware.CorsMiddleware' in settings.MIDDLEWARE
