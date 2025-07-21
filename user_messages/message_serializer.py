from rest_framework import serializers
from .models import Message, Conversation
from accounts.models import UserDetails
from accounts.user_details_serializer import UserDetailSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserDetailSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserDetailSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participants = UserDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = '__all__'
