from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Allow only authenticated users who are participants
    of a conversation to access or modify it.
    """

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Only authenticated users
        if not user or not user.is_authenticated:
            return False

        # For safe methods like GET, HEAD, OPTIONS
        if request.method in SAFE_METHODS:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            elif hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()
        
        # For unsafe methods like PUT, PATCH, DELETE
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            elif hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()

        return False
