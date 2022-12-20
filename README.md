# G3W-ADMIN-AUTHJWT

A proof of concept authentication module through [JSON Web Tokens](https://jwt.io/) for G3W-SUITE.

![cookie-vs-token-auth](https://user-images.githubusercontent.com/9614886/208136975-baf1b19e-9913-44bd-94dd-f5e455b18ea5.png)

## Installation

Install jwt module into [`g3w-admin`](https://github.com/g3w-suite/g3w-admin/tree/v.3.5.x/g3w-admin) applications folder:

```sh
# Install module from github (v1.0.0)
pip3 install git+https://github.com/g3w-suite/g3w-admin-authjwt.git@v1.0.0

# Install module from github (master branch)
# pip3 install git+https://github.com/g3w-suite/g3w-admin-authjwt.git@master

# Install module from local folder (git development)
# pip3 install /g3w-admin/g3w-admin/authjwt

# Install module from PyPi (not yet available)
# pip3 install g3w-admin-authjwt
```

Enable `'authjwt'` module adding it to `G3W_LOCAL_MORE_APPS` list:

```py
# local_settings.py

G3WADMIN_LOCAL_MORE_APPS = [
    ...
    'authjwt'
    ...
]
```

Refer to [g3w-suite-docker](https://github.com/g3w-suite/g3w-suite-docker) repository for more info about running this on a docker instance.

**NB** On Ubuntu Jammy you could get an `UNKNOWN` package install instead of `g3w-admin-authjwt`, you can retry installing it as follows to fix it:

```sh
# Fix: https://github.com/pypa/setuptools/issues/3269#issuecomment-1254507377
export DEB_PYTHON_INSTALL_LAYOUT=deb_system

# And then install again the module
pip3 install ...
```

## Configuration

The following packages are included in this module:

- [django-cors-headers](https://github.com/adamchainz/django-cors-headers#configuration)
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

For the default settings currently applied by this module, see also: [`authjwt/__init__.py`](authjwt/__init__.py) 

## API URLs

Check the [`authjwt/apiurls.py`](authjwt/apiurls.py) file for a comprehensive list and how to use them.

Find out that they are loaded correctly in your project by running the following command in a terminal shell:

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

#### Logout user (optional)

```sh
curl --request POST \
  --url http://localhost:8000/authjwt/api/token/blacklist/ \
  --header 'Content-Type: application/json' \
  --data '{ "refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3MTI3NTg4NSwiaWF0IjoxNjcxMTg5NDg1LCJqdGkiOiIxMTk2NWNiNGFkYjE0ZmEzOTUxYzBhOTkxNDlhZWMwNyIsInVzZXJfaWQiOjJ9.YA4MesWfQcbYip6EhRxZoQAFxoZeBdlJdCrEme8sTc0" }'
```

## Contributing

Steps to follow for local development of this module.

<details>
<summary> Traditional workflow </summary>

Steps to follow in case of a [regular install](https://pip.pypa.io/en/stable/topics/local-project-installs/#regular-installs).

Clone and place the `g3w-admin-authjwt` repository into `g3w-admin` applications folder:

```sh
cd /path/to/your/development/workspace

git clone https://github.com/g3w-suite/g3w-admin.git ./g3w-admin
git clone https://github.com/g3w-suite/g3w-admin-authjwt.git ./g3-admin/g3-admin/authjwt
```

So your folder structure should matches the following:

```sh
.
└── g3w-admin/
    ├── g3w-admin/
    │   ├── authjwt/
    │   │   ├── authjwt/
    │   │   │   ├── __init__.py
    │   │   │   ├── apps.py
    │   │   │   ├── urls.py
    │   │   │   ├── views.py
    │   │   │   └── ...
    │   │   ├── pyproject.toml
    │   │   └── README.md
    │   ├── base/
    │   ├── core/
    │   ├── ...
    │   └── manage.py
    └── README.md
```

Install the `g3w-admin-authjwt` module from the local source folder:

```sh
pip3 install /g3w-admin/g3w-admin/authjwt
```

Then activate the `'authjwt'` module as usual by adding it to `G3W_LOCAL_MORE_APPS` list.

</details>

<details>
<summary> Alternative workflow </summary>

Steps to follow in case of a [editable install](https://pip.pypa.io/en/stable/topics/local-project-installs/#editable-installs).

Clone `g3w-admin` and `g3w-admin-authjwt` repositories into two adjacent folders:

```sh
cd /path/to/your/development/workspace

git clone https://github.com/g3w-suite/g3w-admin.git
git clone https://github.com/g3w-suite/g3w-admin-authjwt.git
```

So your folder structure should matches the following:

```sh
.
├── g3w-admin/
│   ├── g3w-admin/
│   │   ├── base/
│   │   ├── core/
│   │   ├── ...
│   │   └── manage.py
│   └── README.md
│
└── g3w-admin-authjwt/
    ├── authjwt/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── urls.py
    │   ├── views.py
    │   └── ...
    ├── pyproject.toml
    └── README.md
```

Install the `g3w-admin-authjwt` module in editable mode starting from your `g3w-admin` folder:

```sh
cd g3w-admin

python3 -m pip install -e ../g3w-admin-authjwt
```

Then activate the `'authjwt'` module as usual by adding it to `G3W_LOCAL_MORE_APPS` list.

</details>

## Publish

Create a new `git tag` that is appropriate for the version you intend to publish, eg:

```sh
git tag -a v1.0.1
git push origin v1.0.1
```

<details>
<summary> Publishing on the Python Package Index </summary>

Steps to follow when releasing a new software version on [PyPi](https://pypi.org/).

First make sure you have the latest versions of `pip`, `build` and `twine` installed:

```sh
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build
python3 -m pip install --upgrade twine
```

Build the `dist` folder starting from the same directory where `pyproject.toml` is located:

```sh
python3 -m build
```

Upload all to [PyPI](https://pypi.org/) and verify things look right:

```sh
twine upload dist/*
```

</details>

## TODO

Find out if it could be feasible to code a sort of proxy class for the [`rest_framework.permissions.IsAuthenticated`](https://www.django-rest-framework.org/api-guide/permissions/#isauthenticated) (or for the [`rest_framework.viewsets`](https://www.django-rest-framework.org/api-guide/viewsets/)) in order to make use of JWT Authentication with legacy API endpoints that make use of the [`django.contrib.auth.decorators.login_required`](https://docs.djangoproject.com/en/2.2/topics/auth/default/#django.contrib.auth.decorators.login_required) method to check if a user is authenticated, ie:

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

Sample project on how to develop a complete docker stack (backend + frontend):
- [qgis-server-landing-page-plugin](https://github.com/elpaso/qgis-server-landing-page-plugin)

Sample project on how to implement a "simplejwt" extension without using the Django Rest Framework:
- [django-ninja-jwt](https://github.com/eadwinCode/django-ninja-jwt)

Packaging a Python project:
- [PyPA walkthrough](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [`src` layout vs `flat` layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
- [Configuring `setuptools`](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)
- [Configuring `setuptools-scm`](https://github.com/pypa/setuptools_scm/#pyprojecttoml-usage)
- [Using `twine`](https://twine.readthedocs.io/en/latest/)
- [Automate publishing of Python Packages with GitHub Actions](https://www.seanh.cc/2022/05/21/publishing-python-packages-from-github-actions/)

---

**Compatibile with:**
[![g3w-admin version](https://img.shields.io/badge/g3w--admin-3.5-1EB300.svg?style=flat)](https://github.com/g3w-suite/g3w-admin/tree/v.3.5.x)
[![g3w-suite-docker version](https://img.shields.io/badge/g3w--suite--docker-3.5-1EB300.svg?style=flat)](https://github.com/g3w-suite/g3w-suite-docker/tree/v3.5.x)

---

**License:** MPL-2
