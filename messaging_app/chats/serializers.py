from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.SerializerMethodField()
    message_body = serializers.CharField()
    sent_at = serializers.DateTimeField()

    def get_sender_username(self, obj):
        return obj.sender.username

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_username',
            'message_body',
            'sent_at',
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]


class DummySerializer(serializers.Serializer):
    some_field = serializers.CharField()

    def validate_some_field(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Only alphabetic characters allowed.")
        return value
