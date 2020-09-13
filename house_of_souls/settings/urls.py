# Copyright (c) 2020 Yanochka Development LLC, All rights reserved.
# Author Oleg Stadnick <o.stadnick@gmail.com>

from django.urls import path

from . import views

urlpatterns = [
    path('version', views.GetAppVersion.as_view()),
]
