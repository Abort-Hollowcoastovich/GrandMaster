from django.urls import path

from .views import ChatListView, MessageListView, MembersListView, leave_chat


urlpatterns = [
    path('leave/', leave_chat),
    path('members/', MembersListView.as_view()),
    path('messages/', MessageListView.as_view()),
    path('', ChatListView.as_view()),
]
