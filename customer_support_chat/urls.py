from django.urls import path
from .views import ChatRoomView


urlpatterns = [
    path('chat_room/<int:chat_id>/', ChatRoomView.as_view(), name='chat_room_view'),

]