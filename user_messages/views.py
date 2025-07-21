from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .message_serializer import ConversationSerializer, MessageSerializer
from accounts.models import UserDetails

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def conversation_list_create(request):
    if request.method == 'GET':
        user = UserDetails.objects.get(user_id=request.user.id) 
        conversations = Conversation.objects.filter(participants=user)
        serializer = ConversationSerializer(conversations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        participants_ids = request.data.get('participants')
        if not participants_ids:
            return Response({"error": "Participants are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            participants = UserDetails.objects.filter(user_id__in=participants_ids)
            if len(participants) != 2:
                return Response({"error": "One or more users not found"}, status=status.HTTP_404_NOT_FOUND)
        except UserDetails.DoesNotExist:
            return Response({"error": "One or more users not found"}, status=status.HTTP_404_NOT_FOUND)

        conversation = Conversation.objects.filter(participants=participants[0]) \
                                           .filter(participants=participants[1]) \
                                           .distinct().first()

        if conversation:
            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            conversation = Conversation.objects.create()
            conversation.participants.set(participants)
            conversation.save()

            serializer = ConversationSerializer(conversation)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['GET', 'POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def message_list_create(request, conversation_id):
    if request.method == 'GET':
        user = UserDetails.objects.get(email=request.user.email) 

        try:
            conversation = Conversation.objects.get(id=conversation_id, participants=user)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found or you are not a participant"}, status=status.HTTP_404_NOT_FOUND)

        messages = Message.objects.filter(conversation=conversation).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = UserDetails.objects.get(email=request.user.email) 

        content = request.data.get('content')
        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            conversation = Conversation.objects.get(id=conversation_id, participants=user)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation not found or you are not a participant"}, status=status.HTTP_404_NOT_FOUND)

        message = Message(sender=user, conversation=conversation, content=content)
        message.save()

        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
