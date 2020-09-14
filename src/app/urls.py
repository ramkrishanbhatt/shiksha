from django.contrib import admin
from django.urls import include, path
from django.conf import settings

from helpers.health_check import health_check


api_urlpatterns = [
    path('accounts/', include('rest_registration.api.urls')),
]

urlpatterns = [
    path("admin/", admin.site.urls), # ahmad@wavelabs
    # Enables the DRF browsable API page
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("accounts/", include("rest_registration.api.urls")),
    path("health_check/", health_check, name="health_check"),
    path('api/v1/', include(api_urlpatterns)),
]

if settings.ENVIRONMENT == "development":
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
