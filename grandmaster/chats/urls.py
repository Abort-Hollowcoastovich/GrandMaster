from django.urls import path

from .views import ChatListView, MessageListView, MembersListView


urlpatterns = [
    path('members/', MembersListView.as_view()),
    path('messages/', MessageListView.as_view()),
    path('', ChatListView.as_view()),
]
