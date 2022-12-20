# default_app_config = 'auth.jwt.apps.AuthJwtConfig'

from django.conf import settings

settings.MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware'] + settings.MIDDLEWARE 

settings.THIRD_PARTY_APPS += [
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders'
]

settings.REST_FRAMEWORK \
    .setdefault('DEFAULT_AUTHENTICATION_CLASSES', []) \
    .append('rest_framework_simplejwt.authentication.JWTAuthentication')