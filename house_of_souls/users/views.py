from django.contrib import auth
from rest_framework.views import APIView
from rest_framework import (
    exceptions,
    permissions,
    response,
    status,
    viewsets,
    mixins,
)
from . import serializers, permissions as users_perms
from rest_framework.decorators import action


User = auth.get_user_model()


class UsersAPIView(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    APIView,
):
    queryset = User.objects.filter(is_active=True, is_superuser=False, is_staff=False)
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, users_perms.AdminPermission, ]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve' or self.action == 'list':
            return [permissions.IsAuthenticated(), users_perms.ReedOnlyUsersPermission()]
        else:
            return super().get_permissions()

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.AllowAny, ],
        url_path='register',
    )
    def register(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )

    def create(self, request, *args, **kwargs):
        raise exceptions.MethodNotAllowed(
            request.method,
            detail='Not allowed. Register with users/register',
        )

    @action(
        methods=['get', 'put', 'patch'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ],
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(request.user)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated, ],
        url_path='logout'
    )
    def logout(self, request, *args, **kwargs):
        auth.logout(request)
        return response.Response()

    @action(
        methods=['post'],
        detail=False,
        permission_classes=[permissions.AllowAny, ],
        url_path='login',
    )
    def login(self, request, *args, **kwargs):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_user = auth.authenticate(request=request, **serializer.validated_data)
        if auth_user is not None:
            auth.login(request, auth_user)
            return response.Response(
                data=self.get_serializer(request.user).data,
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response('Invalid phone or password', status=status.HTTP_400_BAD_REQUEST)
