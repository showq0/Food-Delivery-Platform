from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Message, Chat
# Create your views here.


class ChatRoomView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id, *args, **kwargs):
        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return Response(
                {"message": "Chat resources not available."},
                status=status.HTTP_404_NOT_FOUND
            )
        messages = Message.objects.filter(chat__id=chat_id) if chat else []
        return render(request, 'chat.html', {
            'chat_id': chat.id,
            'chat_name': chat.__str__(),
            'messages': messages
        })