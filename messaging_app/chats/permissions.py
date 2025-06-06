from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access messages or conversation objects.
    """

    def has_object_permission(self, request, view, obj):
        # Ensure the requesting user is a participant of the conversation
        return request.user in obj.participants.all()
