from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to allow only authenticated users who are participants
    of a conversation to send, view, update, or delete messages.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Check if the user is authenticated
        if not user or not user.is_authenticated:
            return False

        # Check if the user is a participant in the conversation
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # For message objects, check the related conversation
            return user in obj.conversation.participants.all()

        return False
