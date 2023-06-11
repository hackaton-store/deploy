from rest_framework.permissions import BasePermission



class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and request.user == obj.user
    

class IsModerator(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_moderator and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator and request.user.is_authenticated


class IsModeratorOrIsAdminUser(BasePermission):
    
    def has_permission(self, request, view):
        return (request.user.is_moderator or request.user.is_staff)
    
    def has_object_permission(self, request, view, obj):
        return (request.user.is_moderator or request.user.is_staff)


class IsOwnerOrIsModeratorOrIsAdminUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator or request.user.is_staff or (request.user.is_authenticated and request.user == obj.user)
