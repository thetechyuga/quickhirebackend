from django.urls import path
from .views import conversation_list_create, message_list_create

urlpatterns = [
    path('conversations/', conversation_list_create, name='conversation-list-create'),
    path('conversations/<int:conversation_id>/messages/', message_list_create, name='message-list-create'),
]
