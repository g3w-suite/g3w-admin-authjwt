# G3W-ADMIN-AUTHJWT

A proof of concept authentication module through [JSON Web Tokens](https://jwt.io/) for G3W-SUITE.

## Installation

Clone and install jwt module into `/code/g3w-admin/authjwt` directory:

```sh
# docker-entrypoint.sh

...

echo 'Install Auth JWT module'

git clone https://github.com/g3w-suite/g3w-admin-jwt.git /code/g3w-admin/authjwt

pip3 install -r /code/g3w-admin/authjwt/requirements.txt

...
```

Enable `'authjwt'` module adding it to `G3W_LOCAL_MORE_APPS` list:

```py
# settings_docker.py

G3WADMIN_LOCAL_MORE_APPS = [
    ...
    'authjwt'
    ...
]
```

## Dependencies

The following packages are included in this module:

- [django-cors-headers](https://github.com/adamchainz/django-cors-headers)
- [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)

Refer to the official docs for a more comprehensive list of the available settings:

```py
# Customize Django CORS Headers (v3.11.0)
# -------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True # NB: DEVELOPMENT ONLY!

CORS_ALLOWED_ORIGINS = [      # NB: DIFFERENT PORT == DIFFERENT SERVER
     'http://localhost:8080',
     'http://localhost:8081',
     'http://127.0.0.1:8080',
     'http://127.0.0.1:8081',
]
```

```py
# Customize Django REST Framework - Simple JWT (v5.2.2)
# -------------------------------------------

from datetime import timedelta

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_EXPIRATION_DELTA': timedelta(hours=1),        
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7), # 
}

# NB: longer-lived tokens can reduce HTTP traffic
# but they also highlight "health check" issues after
# user logout (given the stateless nature of JWT requests,
# if not handled for example through a "token blacklist",
# the user could still appear as logged-in even after a logout)
# See also:
# - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/blacklist_app.html
# - https://django-rest-framework-simplejwt.readthedocs.io/en/latest/stateless_user_authentication.html
```

## API URLs

Check the [`authjwt/apiurls.py`](apiurls.py) file for a comprehensive list and how to use them.

You can also find out that they are loaded correctly in your app by using the following command in a terminal shell:

```sh
python3 manage.py show_urls
```

```log
/authjwt/api/                   rest_framework.routers.APIRootView                      api-root
/authjwt/api/\.<format>/        rest_framework.routers.APIRootView                      api-root
/authjwt/api/ping/              authjwt.views.PingViewSet                               ping-list
/authjwt/api/ping\.<format>/    authjwt.views.PingViewSet                               ping-list
/authjwt/api/token/             rest_framework_simplejwt.views.TokenObtainPairView      token_obtain_pair
/authjwt/api/token/blacklist/   rest_framework_simplejwt.views.TokenBlacklistView       token_blacklist
/authjwt/api/token/refresh/     rest_framework_simplejwt.views.TokenRefreshView         token_refresh
/authjwt/api/token/verify/      rest_framework_simplejwt.views.TokenVerifyView          token_verify
```

Tip: if you are developing locally use a software like [httpie](https://httpie.io/) (or [postman](https://www.postman.com/)) to import and save the following curl commands for later use:

#### Login user

```sh
curl --request POST \
  --url http://localhost:8000/authjwt/api/token/ \
  --header 'Content-Type: application/json' \
  --data '{ "username":"admin", "password":"admin" }'
```

#### Refresh token

```sh
curl --request POST \
  --url http://localhost:8000/authjwt/api/token/refresh/ \
  --header 'Content-Type: application/json' \
  --data '{ "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTI2NTIyNiwiaWF0IjoxNjcxMTc4ODI2LCJqdGkiOiI3OGFiODU2MjcyZWM0YjAxOWI1Y2M4NTA1ZmNiMTIwOSIsInVzZXJfaWQiOjJ9.AAKmj8I3IN936PrOcxqGmsImWVkFk2AtsFJSE_o4dlY" }'
```

#### Verify token

```sh
curl --request POST \
  --url http://localhost:8000/authjwt/api/token/verify/ \
  --header 'Content-Type: application/json' \
  --data '{ "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTI3NTg4NSwiaWF0IjoxNjcxMTg5NDg1LCJqdGkiOiIxMTk2NWNiNGFkYjE0ZmEzOTUxYzBhOTkxNDlhZWMwNyIsInVzZXJfaWQiOjJ9.YA4MesWfQcbYip6EhRxZoQAFxoZeBdlJdCrEme8sTc0" }'
```

#### Heartbeat (check access to a protected view)

```sh
curl --request GET \
  --url 'http://localhost:8000/authjwt/api/ping/?id=pong' \
  --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjcxMTgyNDIxLCJpYXQiOjE2NzExODIxMjEsImp0aSI6IjI5YjQyN2ZlYjRkMjQ3YmM4NDAzODcyY2VhOTM2NWI5IiwidXNlcl9pZCI6Mn0.P6E7r9BCEFMzkTohJR4EMW1m8wm4DGZ03232mJO6vQI'
```

#### Logout user

```sh
curl --request POST \
  --url http://localhost:8000/authjwt/api/token/blacklist/ \
  --header 'Content-Type: application/json' \
  --data '{ "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTI3NTg4NSwiaWF0IjoxNjcxMTg5NDg1LCJqdGkiOiIxMTk2NWNiNGFkYjE0ZmEzOTUxYzBhOTkxNDlhZWMwNyIsInVzZXJfaWQiOjJ9.YA4MesWfQcbYip6EhRxZoQAFxoZeBdlJdCrEme8sTc0" }'
```

## TODO:

Find out if it could be feasible to code a sort of proxy class for the `rest_framework.permissions.IsAuthenticated` (or for the `rest_framework.viewsets`) in order to make use of JWT Authentication with current API endpoints that already make use of the `django.contrib.auth.decorators.login_required` method to check if a user is authenticated, ie:

```py
# apiurls.py

from django.contrib.auth.decorators import login_required

...

urlpatterns = [

  path(
    'api/some-protected-view/',
    login_required(SomeProtectedView.as_view()), # currently "SomeProtectedView" doesn't support JWT Auth
    name='some-protected-view'
  )

]
```

## Related resources

Code samples on how to implement JWT with Vue and Django Rest Framework:

- [drf-simplejwt-vue](https://github.com/SimpleJWT/drf-SimpleJWT-Vue)
- [drf-jwt-axios-vue](https://daniel.feldroy.com/posts/drf-jwt-axios-vue)
- [article-webapp](https://github.com/smnenko/article-webapp)

Samples project on how to develop a complete docker stack (backend + frontend):
- [qgis-server-landing-page-plugin](https://github.com/elpaso/qgis-server-landing-page-plugin)

Sample project on how to implement a "simplejwt" extension without using the Django Rest Framework:
- [django-ninja-jwt](https://github.com/eadwinCode/django-ninja-jwt)


---

**Compatibile with:**
[![g3w-admin version](https://img.shields.io/badge/g3w--admin-3.5-1EB300.svg?style=flat)](https://github.com/g3w-suite/g3w-admin/tree/v.3.5.x)
[![g3w-suite-docker version](https://img.shields.io/badge/g3w--suite--docker-3.5-1EB300.svg?style=flat)](https://github.com/g3w-suite/g3w-suite-docker/tree/v3.5.x)

---

**License:** MPL-2