from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import StandardResultsSetPagination


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        return self.queryset.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        conversation_id = self.request.query_params.get('conversation_id')
        queryset = Message.objects.filter(conversation__participants=self.request.user)

        if conversation_id:
            queryset = queryset.filter(conversation__id=conversation_id)

        return queryset.order_by('-timestamp')

    def perform_create(self, serializer):
        conversation = serializer.validated_data.get('conversation')
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied(detail="You are not a participant in this conversation.")
        serializer.save(sender=self.request.user)

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user not in message.conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        message = self.get_object()
        if request.user not in message.conversation.participants.all():
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
