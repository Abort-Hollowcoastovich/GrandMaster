from django.urls import path

from .views import ChatListView, MessageListView


urlpatterns = [
    path('messages/', MessageListView.as_view()),
    path('', ChatListView.as_view()),
]
