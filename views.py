from django.views.generic import View
from django.http.response import JsonResponse
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.permissions import IsAuthenticated


class PingViewSet(GenericViewSet, ListModelMixin):
    """
    Helpful class for internal health checks
    for when your server deploys. Typical of AWS
    applications behind ALB which does default 30
    second ping/health checks.
    """
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response(
            status = HTTP_200_OK,
            data   = {
                "id": request.GET.get("id")
            }
        )

# ===================================================
# NB: The following view endpoint doesn't support JWT
# Authentication because it make use of the default
# Django Views class (and not the one provided by
# Django Rest Framework Views instead)
# ===================================================
class SomeProtectedView(View):

    def post(self, *args, **kwargs):
        return JsonResponse({
            'text': 'It Works'
        })