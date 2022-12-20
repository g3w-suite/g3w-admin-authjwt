"""
Add your API routes here.
"""
# API ROOT: /authjwt/

from django.urls import path, include
from django.contrib.auth.decorators import login_required
from authjwt.views import (
    PingViewSet,
    SomeProtectedView
)
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)

router = routers.DefaultRouter()

router.register(
    # ===================================================
    # HEARTBEAT (PING -> PONG)
    # ===================================================
    # To prove authentication for a protected view use
    # the "access" token
    # ===================================================
    # curl \
    #   -H "Authorization: Bearer <JWT__HEADER>.<JWT_PAYLOAD>.<JWT_SIGNATURE>" \
    #   http://localhost:8000/authjwt/api/ping/?id=pong
    # ===================================================
    'ping',
    PingViewSet,
    basename="ping"
)

urlpatterns = [

    path(
        # ===================================================
        # LOGIN USER
        # ===================================================
        # To get a new "access" and a new "refresh" token
        # send the client credentials (username and password)
        # ===================================================
        # curl \
        #   -X POST \
        #   -H "Content-Type: application/json" \
        #   -d '{"username": "admin", "password": "admin"}' \
        #   http://localhost:8000/authjwt/api/token/
        # ===================================================
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        # ===================================================
        # REFRESH TOKEN
        # ===================================================
        # To get a new "access" token send the "refresh" token 
        # ===================================================
        # curl \
        #   -X POST \
        #   -H "Content-Type: application/json" \
        #   -d '{"refresh":"<JWT__HEADER>.<JWT_PAYLOAD>.<JWT_SIGNATURE>"}' \
        #   http://localhost:8000/authjwt/api/token/refresh/
        # ===================================================
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    path(
        # ===================================================
        # VERIFY TOKEN
        # ===================================================
        # Check token validity (eg. expired "access" token)
        # ===================================================
        # curl \
        #   -X POST \
        #   -H "Content-Type: application/json" \
        #   -d '{"token":"<JWT_HEADER>.<JWT_PAYLOAD>.<JWT_SIGNATURE>"}' \
        #   http://localhost:8000/authjwt/api/token/verify/
        # ===================================================
        'api/token/verify/',
        TokenVerifyView.as_view(),
        name='token_verify'
    ),

    path(
        # ===================================================
        # LOGOUT USER
        # ===================================================
        # Force logout user by invalidating its token
        # (reccomended when using longer-lived tokens).
        #
        # You should set up a daily cron job on your server,
        # calling the "python3 manage.py flushexpiredtokens"
        # command which will delete any tokens from the
        # outstanding list and blacklist that have expired.
        # ===================================================
        # curl \
        #   -X POST \
        #   -H "Content-Type: application/json" \
        #   -d '{"refresh":"<JWT_HEADER>.<JWT_PAYLOAD>.<JWT_SIGNATURE>"}' \
        #  http://localhost:8000/authjwt/api/token/blacklist/
        # ===================================================
        'api/token/blacklist/',
        TokenBlacklistView.as_view(),
        name='token_blacklist'
    ),

    # ===================================================
    # NB: The following endpoint doesn't support JWT
    # Authentication because internally it make use of
    # the default Django Views class (and not the one
    # provided by Django Rest Framework Views instead)
    # ===================================================
    # path(
    #     'api/some-protected-view/',
    #     login_required(SomeProtectedView.as_view()),
    #     name='some-protected-view'
    # ),

    path(
        'api/',
        include(router.urls)
    )

]