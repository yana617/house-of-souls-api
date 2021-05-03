# Copyright (c) 2020 Yanochka Development LLC, All rights reserved.
# Author Oleg Stadnick <o.stadnick@gmail.com>

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='HOUSE OF SOULS API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger')),
    path('api/', include('settings.urls')),
    path('api/', include('users.urls')),
]
