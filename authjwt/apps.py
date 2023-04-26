from django.conf import settings
from django.apps import AppConfig


class AuthJwtConfig(AppConfig):
    name = 'authjwt'
    verbose_name = "JWT Auth"

    settings.MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')

    settings.THIRD_PARTY_APPS += [
        'rest_framework_simplejwt',
        'rest_framework_simplejwt.token_blacklist',
        'corsheaders'
    ]

    settings.REST_FRAMEWORK \
        .setdefault('DEFAULT_AUTHENTICATION_CLASSES', []) \
        .append('rest_framework_simplejwt.authentication.JWTAuthentication')
