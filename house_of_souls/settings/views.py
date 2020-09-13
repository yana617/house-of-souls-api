# Copyright (c) 2020 Yanochka Development LLC, All rights reserved.
# Author Oleg Stadnick <o.stadnick@gmail.com>

import os

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from utils import constants


class GetAppVersion(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            with open(os.path.join(settings.BASE_DIR, '../VERSION.txt'), 'r') as f:
                data = {
                    'version': f.readline().rstrip('\n')
                }
        except FileNotFoundError:
            data = {
                'version': constants.UNKNOWN_APP_VERSION
            }
        return Response(data=data, status=status.HTTP_200_OK)
