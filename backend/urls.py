from django.contrib import admin
from django.urls import path, include
from api.views import (
    UserViewSet,
    EspecialidadeViewSet,
    MedicoViewSet,
    AgendaViewSet,
    ConsultaViewSet,
    CustomObtainAuthToken,
)
from rest_framework import routers

admin.site.site_header = "Medicar Dashboard"

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="users-viewset")
router.register("especialidades", EspecialidadeViewSet, basename="especialidades-viewset")
router.register("medicos", MedicoViewSet, basename="medicos-viewset")
router.register("agendas", AgendaViewSet, basename="agendas-viewset")
router.register("consultas", ConsultaViewSet, basename="consultas-viewset")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api-token-auth/", CustomObtainAuthToken.as_view(), name="api_token_auth"),
    path("api-auth/", include("rest_framework.urls")),
]

