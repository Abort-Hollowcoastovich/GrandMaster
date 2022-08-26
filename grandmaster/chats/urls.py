from django.urls import path

from .views import ChatListView, MessageListView, MembersListView, leave_chat, remove_member


urlpatterns = [
    path('remove/', remove_member),
    path('leave/', leave_chat),
    path('members/', MembersListView.as_view()),
    path('messages/', MessageListView.as_view()),
    path('', ChatListView.as_view()),
]
