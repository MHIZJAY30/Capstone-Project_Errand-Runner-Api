from rest_framework import permissions

class IsRequester(permissions.BasePermission):
    "Only allow the requester to modify their errand"
    def has_object_permission(self, request, view, obj):
        return obj.requester == request.user

class IsParticipant(permissions.BasePermission):
    "Only allow participants (requester or runner) to access"
    def has_object_permission(self, request, view, obj):
        return request.user in [obj.requester, obj.runner]

class IsRunner(permissions.BasePermission):
    "Only allow the runner to perform action"
    def has_object_permission(self, request, view, obj):
        return obj.runner == request.user

class IsCompletedErrand(permissions.BasePermission):
    "Only allow actions on completed errands"
    def has_object_permission(self, request, view, obj):
        return obj.status == 'completed'