from rest_framework import permissions


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_admin


class VolunteerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_volunteer


class ReedOnlyUsersPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if view.action == 'retrieve':
            return True
        return user.is_volunteer or user.is_admin

    def has_object_permission(self, request, view, obj):
        user = request.user
        if view.action == 'retrieve' and obj == user:
            return True
        return user.is_volunteer or user.is_admin
