from django.urls import path

from .views import ChatListView, MessageListView, MembersListView, leave_chat, remove_member, ChatDetailView

urlpatterns = [
    path('<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('remove/', remove_member),
    path('leave/', leave_chat),
    path('members/', MembersListView.as_view()),
    path('messages/', MessageListView.as_view()),
    path('', ChatListView.as_view()),
]
